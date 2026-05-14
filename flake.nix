{
  description = "Logo Scraper";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python312;

      nativeBuildInputs = with pkgs; [
        python
        playwright-driver.browsers
        postgresql
      ];

      buildInputs = with pkgs; [];

    in {
      devShells.default = pkgs.mkShell {
        inherit nativeBuildInputs buildInputs;
        env = {
          PLAYWRIGHT_BROWSERS_PATH = pkgs.playwright-driver.browsers;
          PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD = "1";
          LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
        };
        shellHook = ''
          export PGDATA="$PWD/pgdata"
          export PGHOST="$PWD/pgdata"
          if [ ! -d "$PGDATA" ]; then
            echo "Initialising local postgres..."
            initdb --no-locale --encoding=UTF8
          fi
          pg_ctl start -l "$PGDATA/postgres.log" -o "--unix_socket_directories=$PGDATA"
          trap "pg_ctl stop" EXIT
        '';
      };


      packages.default = python.pkgs.buildPythonApplication {
        pname = "logo-scraper";
        version = "0.0.0";
        format = "setuptools";
        src = ./.;
        doCheck = false;
        inherit nativeBuildInputs buildInputs;
        propagatedBuildInputs = with python.pkgs; [
          playwright
          beautifulsoup4
        ];
      };
    });
}