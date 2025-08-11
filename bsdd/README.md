
- task: https://github.com/statnett/CIM4Enterprise/issues/8 . Convert to BSDD:
  - `Switch, SwitchInfo` and their parent classes (eg `IdentifiedObject, PowerSystemResource, Asset, AssetInfo`)
  - All their properties (data and enum props but not Relations)
  - All their enumerations
- [bsdd-import-model.json](https://raw.githubusercontent.com/buildingSMART/bSDD/refs/heads/master/Model/Import%20Model/bsdd-import-model.json): template JSON for BSDD import
- `bsdd-import-model.yaml`: same but in YAML: easier to edit and allows comments and commenting-out of lines

TODO:
- `cim-bsdd-import.yaml`: mapping of a few CIM clases (eg `cim:Switch, SwitchInfo, Asset`) and all their properties 
- `cim-bsdd-import.json`: same but in JSON
- JSONLD context with `"@vocab: bsdd"` and a few more term definitions to map all JSON terms (eg `Code <-> bsdd:Code`)
- JSONLD frame to guide the nesting: `Class>ClassProperty, ClassProperty>AllowedValues, Property>AllowedValues`
- `cim-bsdd-import.ttl`: converted example `cim-bsdd-import.json`
- `cim-bsdd-export.ru`: SPARQL CONSTRUCT query to extract the selected elements.
  It should emit exactly the same data for `Property` and `ClassProperty`: the latter is duplicative, and we don't need any variation of prop characteristics
- `Makefile`: automate the whole process of running the query and making JSON
