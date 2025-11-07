CIM to bSDD transformation was implemented as an answer to BIM-CIM immediate integration requirements, described in more detail in [BIM CIM Integration Requirements and Technical Design](https://github.com/statnett/Talk2PowerSystem/wiki/BIM-CIM-Integration-Requirements-and-Technical-Design#immediate-priorities).

The information flow required for the transformation is illustrated on the following sequence diagram:

![CIM-bSDD_squence.png](../CIM-bSDD_sequence.png)

1. The transformation tool is initiated with the following arguments:
   - GraphDB URI
   - username
   - password
   - GraphDB repository
2. Class data retrieval query is loaded from the filesystem (`./SPARQL/retrieve-class-info.rq`)
3. Query is sent to the GraphDB repository via REST API
4. HTTP GET Request to buildingSMART bSDD API to retrieve QUDT to bSDD units map is sent.
5. Upon retrieval of class data and unit map data, both datasets are  is post-processed to the format required to prepare bSDD dictionary.
6. Properties data retrieval query is loaded from the filesystem (`./SPARQL/retrieve-properties-info.rq`)
7. Upon retrieval of properties data and unit map data, both datasets are post-processed to the format required to prepare bSDD dictionary. QUDT dimensiton vector URLs are mapped to the bSDD unit format, using the following regular expression: "A([0-9-]+)E([0-9-]+)L([0-9-]+)I([0-9-]+)M([0-9-]+)H([0-9-]+)T([0-9-]+)D([0-9-]+)", "$3 $5 $7 $2 $6 $1 $4"

Using this vector as example:

```
qkdv:A-1E0L-3I0M0H0T0D0
  qudt:dimensionExponentForAmountOfSubstance -1 ;
  qudt:dimensionExponentForElectricCurrent 0 ;
  qudt:dimensionExponentForLength -3 ;
  qudt:dimensionExponentForLuminousIntensity 0 ;
  qudt:dimensionExponentForMass 0 ;
  qudt:dimensionExponentForThermodynamicTemperature 0 ;
  qudt:dimensionExponentForTime 0 ;
  qudt:dimensionlessExponent 0 ;
```

The mapping of a physical quantity, specify dimension according to International_System_of_Quantities, as defined in ISO 80000-1. The order is:

- length
- mass
- time
- electric current
- thermodynamic temperature
- amount of substance
- luminous intensity

8. Post-processed and unit mapped class and properties datasets are merged with the dictionary metadata.
9. The whole dictionary (metadata, class data, properties data) is saved to the filesystem (`cim-bsdd.json`).

Requirements for the transformation script installation are described in [the tool readme](Python/cim_to_bsdd/README.md).



Tasks description:

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
