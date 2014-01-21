# TODO
# - vim subpackage
# - zsh completions subpackage
# - emacs subpackage
#
# Conditional build:
%bcond_with	bootstrap		# do bootstrap build
%bcond_without	doc			# don't build doc

Summary:	A small build system with a focus on speed
Name:		ninja
Version:	1.0.0
Release:	2
License:	Apache v2.0
Group:		Development/Tools
Source0:	https://github.com/martine/ninja/archive/v%{version}.tar.gz
# Source0-md5:	51f58e418d215ffc165cb9c5ad6cf0d7
URL:		http://martine.github.com/ninja/
Source1:	%{name}.vim
%{?with_doc:BuildRequires:	asciidoc}
BuildRequires:	libstdc++-devel
%{!?with_bootstrap:BuildRequires:	ninja}
BuildRequires:	rpmbuild(macros) >= 1.673
Obsoletes:	ninja-build < 1.0.0-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ninja is a small build system with a focus on speed. It differs from
other build systems in two major respects: it is designed to have its
input files generated by a higher-level build system, and it is
designed to run builds as fast as possible.

%package -n bash-completion-%{name}
Summary:	bash-completion for %{name}
Group:		Applications/Shells
Requires:	%{name}
Requires:	bash-completion >= 2.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-%{name}
bash-completion for %{name}.

%package doc
Summary:	Manual for %{name}
Summary(fr.UTF-8):	Documentation pour %{name}
Summary(it.UTF-8):	Documentazione di %{name}
Summary(pl.UTF-8):	Podręcznik dla %{name}
Group:		Documentation
# noarch subpackages only when building with rpm5
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Documentation for %{name}.

%description doc -l fr.UTF-8
Documentation pour %{name}.

%description doc -l it.UTF-8
Documentazione di %{name}.

%description doc -l pl.UTF-8
Dokumentacja do %{name}.

%prep
%setup -q

%build
export CXX="%{__cxx}"
export CFLAGS="%{rpmcflags}"

%if %{with bootstrap}
./bootstrap.py --verbose -- --debug
export PATH=$(pwd):$PATH
%else
./configure.py
ninja -v
%endif

# build manual
%{?with_doc:ninja -v manual}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
# TODO: Install ninja_syntax.py?
install -p %{name} $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{bash_compdir}
cp -p misc/bash-completion $RPM_BUILD_ROOT%{bash_compdir}/%{name}

%if 0
install -p -d $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
install -p misc/ninja-mode.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/ninja-mode.el

install -p -d $RPM_BUILD_ROOT%{_datadir}/vim/vimfiles/syntax
install -p misc/ninja.vim $RPM_BUILD_ROOT%{_datadir}/vim/vimfiles/syntax/ninja.vim
install -p -d $RPM_BUILD_ROOT%{_datadir}/vim/vimfiles/ftdetect
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/vim/vimfiles/ftdetect/ninja.vim

install -p -d $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions
install -p misc/zsh-completion $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions/_ninja
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_bindir}/ninja

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/%{name}

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/manual.html
%endif

%if 0
# emacs
%{_datadir}/emacs/site-lisp/ninja-mode.el
# vim
%{_datadir}/vim/vimfiles/syntax/ninja.vim
%{_datadir}/vim/vimfiles/ftdetect/ninja.vim

# zsh does not have a -filesystem package
%{_datadir}/zsh/
%endif
