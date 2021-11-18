{
  description = "Collect related papers and filter by keywords.";

  inputs = {
    nixpkgs = { url = "github:nixos/nixpkgs/d189bf92f9be23f9b0f6c444f6ae29351bb7125c"; };
    utils = { url = "github:numtide/flake-utils"; };
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, utils, gitignore, ... }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        python = pkgs.python39;
        projectDir = gitignore.lib.gitignoreSource ./.;
        overrides = pkgs.poetry2nix.overrides.withDefaults (final: prev: {
          # Python dependency overrides go here
        });

        packageName = "collector";
      in
      {
        packages.${packageName} = pkgs.poetry2nix.mkPoetryApplication {
          inherit python projectDir overrides;
          # Non-Python runtime dependencies go here
          propogatedBuildInputs = [ ];
        };

        defaultPackage = self.packages.${system}.${packageName};

        devShell = pkgs.mkShell {
          buildInputs = [
            # python
            (pkgs.poetry2nix.mkPoetryEnv {
              inherit python projectDir overrides;
              editablePackageSources = {
                package = ./.;
              };
            })
            pkgs.poetry
          ];
        };
      });
}
