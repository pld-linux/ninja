#
# Conditional build:
%bcond_with	bootstrap	# do bootstrap build
%bcond_without	doc		# HTML documentation

Summary:	A small build system with a focus on speed
Summary(pl.UTF-8):	Mały system budowania ukierunkowany na szybkość
Name:		ninja
Version:	1.7.2
Release:	1
License:	Apache v2.0
Group:		Development/Tools
#Source0Download: https://github.com/ninja-build/ninja/releases
Source0:	https://github.com/ninja-build/ninja/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7b482218757acbaeac4d4d54a3cd94e1
URL:		http://ninja-build.org/
%{?with_doc:BuildRequires:	asciidoc}
BuildRequires:	libstdc++-devel
%{!?with_bootstrap:BuildRequires:	ninja}
BuildRequires:	python >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.673
Obsoletes:	ninja-build < 1.0.0-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ninja is a small build system with a focus on speed. It differs from
other build systems in two major respects: it is designed to have its
input files generated by a higher-level build system, and it is
designed to run builds as fast as possible.

%description -l pl.UTF-8
Ninja to mały system budowania ukierunkowany na szybkość. Różni się od
innych systemów budowania pod dwoma głównymi względami: jest
zaprojektowany, aby przyjmować pliki wejściowe wygenerowane przez
system budowania wyższego poziomu oraz tak, aby budowanie przebiegało
jak najszybciej.

%package doc
Summary:	Manual for Ninja build system
Summary(pl.UTF-8):	Podręcznik do systemu budowania Ninja
Group:		Documentation
# noarch subpackages only when building with rpm5
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Manual for Ninja build system.

%description doc -l pl.UTF-8
Podręcznik do systemu budowania Ninja.

%package -n bash-completion-%{name}
Summary:	Bash completion for ninja command
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów polecenia ninja
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-%{name}
Bash completion for ninja command.

%description -n bash-completion-%{name} -l pl.UTF-8
Bashowe dopełnianie parametrów polecenia ninja.

%package -n zsh-completion-%{name}
Summary:	zsh completion for ninja command
Summary(pl.UTF-8):	Dopełnianie parametrów polecenia ninja dla powłoki zsh
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n zsh-completion-%{name}
zsh completion for ninja command.

%description -n zsh-completion-%{name} -l pl.UTF-8
Dopełnianie parametrów polecenia ninja dla powłoki zsh.

%package -n emacs-ninja-mode
Summary:	Ninja mode for Emacs
Summary(pl.UTF-8):	Tryb Ninja dla Emacsa
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}
Requires:	emacs
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n emacs-ninja-mode
Ninja mode for Emacs.

%description -n emacs-ninja-mode -l pl.UTF-8
Tryb Ninja dla Emacsa.

%prep
%setup -q

%build
export CXX="%{__cxx}"
export CFLAGS="%{rpmcxxflags} -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"

./configure.py \
	%{?with_bootstrap:--bootstrap} \
	--verbose

%if %{without bootstrap}
ninja -v
%endif

# build manual
%{?with_doc:./ninja -v manual}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install -p %{name} $RPM_BUILD_ROOT%{_bindir}
# TODO: Install ninja_syntax.py as python module?

install -d $RPM_BUILD_ROOT%{bash_compdir}
cp -p misc/bash-completion $RPM_BUILD_ROOT%{bash_compdir}/%{name}

install -d $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
install -p misc/ninja-mode.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/ninja-mode.el

install -d $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions
install -p misc/zsh-completion $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions/_ninja

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_bindir}/ninja

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/manual.html
%endif

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/ninja

%files -n zsh-completion-%{name}
%defattr(644,root,root,755)
%{_datadir}/zsh/site-functions/_ninja

%files -n emacs-ninja-mode
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/ninja-mode.el
