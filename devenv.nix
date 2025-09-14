{ pkgs, lib, config, ... }: {
  languages = {
    python = {
      enable = true;
      uv = {
        enable = true;
        sync.enable = true;
      };
    };
    javascript.enable = true;
  };
  packages = [ 
    pkgs.git
    pkgs.zsh
  ];
  enterShell = ''
    echo "Python environment managed by uv."
        echo "Node.js environment ready for Svelte."'';
}

