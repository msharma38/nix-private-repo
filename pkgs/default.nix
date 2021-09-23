{ stdenv, fetchurl, libpng,
  mpiEnabled ? false,
  fftw,
  openmpi
}:

stdenv.mkDerivation rec {
  version = "16Feb16";
  name = "lammps-${version}";

  src = fetchurl {
    url = "http://downloads.sourceforge.net/project/lammps/lammps-16Feb16.tar.gz";
    sha256 = "058459f3053cca0b8c0fdd05cca7acab6ac00934c6da8c9008aa0f55fb5ceefb";
  };

  buildInputs = [ fftw ]
  ++ (stdenv.lib.optionals mpiEnabled [ openmpi ]);

  # Make serial version for now
  builder = builtins.toFile "builder.sh" "
    source $stdenv/setup
    tar xzf $src
    cd lammps-*/src
    make mode=exe serial SHELL=$SHELL
    make mode=shlib serial SHELL=$SHELL
    mkdir -p $out/bin
    cp lmp_serial $out/bin/lammps
    mkdir -p $out/lib
    cp liblammps* $out/lib/
    ";

  meta = {
    description = "Classical Molecular Dynamics simulation code";
    longDescription = ''
      LAMMPS is a classical molecular dynamics simulation code designed to
      run efficiently on parallel computers. It was developed at Sandia
      National Laboratories, a US Department of Energy facility, with
      funding from the DOE. It is an open-source code, distributed freely
      under the terms of the GNU Public License (GPL).
      '';
    homepage = "http://lammps.sandia.gov";
    license = stdenv.lib.licenses.gpl2;
    platforms = stdenv.lib.platforms.linux;
  };
}
