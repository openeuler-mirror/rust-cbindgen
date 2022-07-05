%global debug_package %{nil}
%global crate_name cbindgen
%global rustflags -Clink-arg=-Wl,-z,relro,-z,now

Name:        rust-cbindgen
Version:        0.24.3
Release:        1
Summary:        Tool for generating C bindings to Rust code
License:        MPL-2.0
URL:            https://crates.io/crates/cbindgen
Source0:        %{crate_name}-%{version}.tar.xz
Source1:        vendor.tar.xz
Source2:        cargo_config
BuildRequires:  cargo >= 1.30.0
BuildRequires:  rust >= 1.30.0

%description
Tool for generating C bindings to Rust code.

%prep
%setup -q -T -b 0 -n %{crate_name}-%{version}
%setup -q -D -T -a 1 -n %{crate_name}-%{version}
mkdir cargo-home
cp %{SOURCE2} cargo-home/config

%build
export RUSTFLAGS="%{rustflags}"
export CARGO_HOME=`pwd`/cargo-home/

cargo build --release

%install
# rustflags must be exported again at install as cargo build will
# rebuild the project if it detects flags have changed (to none or other)
export RUSTFLAGS="%{rustflags}"
# install stage also requires re-export of 'cargo-home' or cargo
# will try to download source deps and rebuild
export CARGO_HOME=`pwd`/cargo-home/
# cargo install appends /bin to the path
cargo install --root=%{buildroot}%{_prefix} --path .
# remove spurious files
rm -f %{buildroot}%{_prefix}/.crates.toml
rm -f %{buildroot}%{_prefix}/.crates2.json

%files
%license LICENSE
%{_bindir}/cbindgen

%changelog
* Wed Jul 06 2022 jchzhou <jchzhou@outlook.com> - 0.24.3-1
- Init package from openSUSE
- Credit: Wolfgang Rosenauer (wolfgang@rosenauer.org)
- Link: https://build.opensuse.org/package/show/devel:languages:rust/rust-cbindgen
