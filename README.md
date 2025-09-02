# Newton Assets

This repository holds a collection of permissively licensed assets for use with Newton.

Contributors should store possibly large simulation assets such as models, textures, datasets, or pre-trained policies in this repository to keep code-development repositories small.

## Contributing to Assets

* Before proposing to add any assets to the Newton project, make sure that the assets are properly licensed for use and distribution. If you are unsure about the license, open a new [issue](https://github.com/newton-physics/newton-assets/issues).
* In addition to the pull request to the code repository that relies on the new assets, open a corresponding pull request in this assets repository.
* Follow the file structure of existing assets, i.e. the parent folder should be `manufacturer_robot_model`, and contain
    * appropriately named subfolders that contain the different asset types and formats
    * a LICENSE file with an appropriate, permissive license, see first point above
    * a README.md describing the asset and its origins, and provides a changelog, if applicable
* Have a signed CLA on file (see [Legal Requirements](https://github.com/newton-physics/newton-governance/blob/main/CONTRIBUTING.md#legal-requirements)).
* Have the pull request approved by a [Project Member](https://github.com/newton-physics/newton-governance/blob/main/CONTRIBUTING.md#project-members) and merged into the asset repository.

## General Guidelines and Legal

Please refer to [the contribution guidelines](https://github.com/newton-physics/newton-governance/blob/main/CONTRIBUTING.md) in the `newton-governance` repository for general information, project membership, and legal requirements for making contributions to Newton.
