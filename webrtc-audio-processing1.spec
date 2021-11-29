# NOTE:
# f.d.o source is meant to be a more Linux packaging friendly copy of the
# AudioProcessing module from the WebRTC[1] project. The ideal case is that we
# make no changes to the code to make tracking upstream code easy.
# [1] http://code.google.com/p/webrtc/
#
# Conditional build:
%bcond_without	neon		# ARM NEON instructions
%bcond_with	sse2		# SSE2 instructions

%ifnarch armv7l armv7hl armv7hnl armv8l armv8hl armv8hnl armv8hcnl aarch64
%undefine	with_neon
%endif
%ifarch pentium4 %{x8664} x32
%define		with_sse2	1
%endif

Summary:	WebRTC Audio Processing library
Summary(pl.UTF-8):	Biblioteka WebRTC Audio Processing
Name:		webrtc-audio-processing1
Version:	1.0
Release:	3
License:	BSD
Group:		Libraries
Source0:	https://freedesktop.org/software/pulseaudio/webrtc-audio-processing/webrtc-audio-processing-%{version}.tar.gz
# Source0-md5:	8ee1b2f3e615c6c2024951c559a9913a
Patch0:		%{name}-abseil.patch
Patch1:		%{name}-nosimd.patch
URL:		https://www.freedesktop.org/software/pulseaudio/webrtc-audio-processing/
BuildRequires:	abseil-cpp-devel >= 20200923
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	meson >= 0.54
BuildRequires:	ninja >= 1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WebRTC is an open source project that enables web browsers with
Real-Time Communications (RTC) capabilities via simple Javascript
APIs. The WebRTC components have been optimized to best serve this
purpose. WebRTC implements the W3C's proposal for video conferencing
on the web.

%description -l pl.UTF-8
WebRTC to projekt o otwartych źródłach dodający obsługę komunikacji
w czasie rzeczywistym (RTC - Real-Time Communications) poprzez proste
API JavaScriptu. Komponenty WebRTC zostały zoptymalizowane, aby jak
najlepiej sprawdzały się w tym zastosowaniu. WebRTC implementuje
propozycje W3C do wideokonferencji w sieci.

%package devel
Summary:	Header files for WebRTC Audio Processing library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki WebRTC Audio Processing
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	abseil-cpp-devel >= 20200923
Requires:	libstdc++-devel >= 6:5

%description devel
This package contains the header files needed to develop programs
which make use of WebRTC Audio Processing library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
wykorzystujących bibliotekę WebRTC Audio Processing.

%package static
Summary:	Static WebRTC Audio Processing library
Summary(pl.UTF-8):	Biblioteka statyczna WebRTC Audio Processing
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static WebRTC Audio Processing library.

%description static -l pl.UTF-8
Biblioteka statyczna WebRTC Audio Processing.

%prep
%setup -q -n webrtc-audio-processing-%{version}
%patch0 -p1
%patch1 -p1

%ifarch %{ix86}
%if %{without sse2}
# add -DPFFFT_SIMD_DISABLE
%{__sed} -i -e 's/have_arm and not have_neon.*/& or true/' webrtc/third_party/pffft/meson.build
%endif
%endif

%build
%if %{with sse2}
CFLAGS="%{rpmcflags} -msse2"
CXXFLAGS="%{rpmcxxflags} -msse2"
%endif
%meson build \
	-Dneon=%{?with_neon:runtime}%{!?with_neon:no}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.md webrtc/PATENTS
%attr(755,root,root) %{_libdir}/libwebrtc-audio-coding-1.so.0
%attr(755,root,root) %{_libdir}/libwebrtc-audio-processing-1.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwebrtc-audio-coding-1.so
%attr(755,root,root) %{_libdir}/libwebrtc-audio-processing-1.so
%{_includedir}/webrtc-audio-processing-1
%{_pkgconfigdir}/webrtc-audio-coding-1.pc
%{_pkgconfigdir}/webrtc-audio-processing-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libwebrtc-audio-coding-1.a
%{_libdir}/libwebrtc-audio-processing-1.a
