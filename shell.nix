let
  pkgs = import <nixpkgs> {};
  # unstable = import <nixos-unstable> {};
in
let
  my-python-packages = python-packages: with python-packages; [
    pyqt6
  ];
  python-with-my-packages = pkgs.python3.withPackages my-python-packages;
in
pkgs.mkShell {
  buildInputs = [
    python-with-my-packages
    pkgs.qt6.full
  ];
}
