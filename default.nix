{ system ? builtins.currentSystem }:                                                   
                                                                                   
let                                                                                    
   pkgs = import <nixpkgs> { inherit system; };                                         
                                                                                   
   callPackage = pkgs.lib.callPackageWith (pkgs // self);                               
                                                                                   
   self = {                                                                             
      sc-file-watcher = callPackage ./pkgs/sc-file-watcher { };    
      lammps =  callPackage ./pkgs/lammps { };
      hello =  callPackage ./pkgs/hello { };
      openbrf =  callPackage ./pkgs/openbrf { };
      calc =  callPackage ./pkgs/calc { };
      form = callPackage ./pkgs/form { };
      test = callPackage ./pkgs/test { };
      

   };                                                                                   
in self 
