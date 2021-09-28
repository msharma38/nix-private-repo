{ pkgs ? import <nixpkgs> {} }:

pkgs.python3Packages.buildPythonApplication {
  pname = "testapp";
  src = ./.;
  version = "0.1";
  propagatedBuildInputs = [ pkgs.python3Packages.flask ];
}
