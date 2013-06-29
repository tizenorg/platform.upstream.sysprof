# spec file for package sysprof, based on one from SUSE
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2013 Intel Corporation
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# norootforbuild

%define enable_gui 0

Name:           sysprof
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  binutils-devel
BuildRequires:  glib2-devel
%if 0%{?enable_gui}
BuildRequires:  gtk2-devel
BuildRequires:  libgladeui-devel
%endif
ExclusiveArch:  %ix86 x86_64
Summary:        Sampling CPU profiler
Version:        1.2.0
Release:        0
License:        GPL v2 or later
Group:          Development/Tools/Debuggers
Url:            http://sysprof.com/
Source:         sysprof-%version.tar.bz2
Source1001: 	sysprof.manifest
Recommends:     sysprof-cli

%description
Sysprof is a sampling CPU profiler for Linux.

%package cli
Summary:        Sampling CPU profiler (CLI)

%description cli
Sysprof is a sampling CPU profiler for Linux.
This package contains the command-line data-collection part only.

%prep
%setup -q -n sysprof-%version
cp %{SOURCE1001} .

%build
NOCONFIGURE=1 ./autogen.sh
%configure CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
make

%install
rm -rf $RPM_BUILD_ROOT
%make_install
# unnecessary, sysprof now uses the standard kernel interface for profiling
# (since 1.1; compare with Debian patches)
rm -r $RPM_BUILD_ROOT/etc/udev/rules.d
%if 0%{?enable_gui}
# keep the icons and Glade files
%else
rm $RPM_BUILD_ROOT%{_datadir}/pixmaps/*.png
rm $RPM_BUILD_ROOT%{_datadir}/sysprof/sysprof.glade
rmdir $RPM_BUILD_ROOT%{_datadir}/sysprof
rmdir $RPM_BUILD_ROOT%{_datadir}/pixmaps
rmdir $RPM_BUILD_ROOT%{_datadir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if 0%{?enable_gui}
%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_bindir}/sysprof
%dir %{_datadir}/sysprof
%{_datadir}/applications/sysprof.desktop
%{_datadir}/sysprof/sysprof.glade
%{_datadir}/pixmaps/*.png
%endif

%files cli
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_bindir}/sysprof-cli
