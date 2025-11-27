CIM to bSDD transformation was implemented as an answer to BIM-CIM immediate integration requirements, described in more detail in [BIM CIM Integration Requirements and Technical Design](https://github.com/statnett/Talk2PowerSystem/wiki/BIM-CIM-Integration-Requirements-and-Technical-Design#immediate-priorities).

The information flow required for the transformation is illustrated on the following sequence diagram:

![CIM-bSDD_squence.png](../CIM-bSDD_sequence.png)

1. The transformation tool is initiated with the following arguments:
   - GraphDB URI
   - username
   - password
   - GraphDB repository
2. Class data retrieval query is loaded from the filesystem (`./SPARQL/retrieve-class-info.rq`)
   The query has form of SPARQL CONSTRUCT with the target graph pattern, returned by it matching [required keys form bSDD](https://github.com/buildingSMART/bSDD/blob/master/Documentation/bSDD%20JSON%20import%20model.md#class):
   - Code
   - Name
   - ClassType
   - Definition
   - ParentClassCode
   - CreatorLanguageIsoCode
   - OwnedUri
   - Status
   - ClassProperties (DatatypeProperty and enumeration ObjectProperties properties with class and its superclasses in the domain), each of which includes pattern to return:
      - Code
      - PropertyUri
      - Description
      - Unit
      - OwnedUri
      - PropertyType
      - AllowedValues, each of which includes pattern to return:
         - Code
         - Value
         - Description
         - OwnedUri
   The WHERE clause contains provided calass VALUES for the scope of the target graph: `cim:AssetInfo cim:IdentifiedObject cim:CableInfo
cim:WireInfo cim:OverheadWireInfo cim:ShuntCompensatorInfo cim:SwitchInfo cim:TapChangerInfo cim:TransformerEndInfo cim:TransformerTankInfo cim:WireSpacingInfo cim:ProductAssetModel cim:Manufacturer cim:Asset cim:AssetContainer cim:EndDevice cim:Meter cim:Structure cim:AssetOrganisationRole cim:AssetOwner cim:AssetModelUsageKind cim:OrganisationRole cim:SinglePhaseKind cim:TransformerMeshImpedance cim:UnitMultiplier cim:UnitSymbol cim:WireInsulationKind cim:WirePhaseInfo cim:WirePosition cim:WireUsageKind cim:InUseStateKind cim:LifecycleDate cim:PowerSystemResource cim:UsagePoint` and the following mappings from CIM ontology to the bSDD variables above:


         | RDF | bSDD |
         | -------- | ------- |
         | class IRI with the value of PREFIX removed | class Code |
         | class rdfs:label | class Name |
         | class rdfs:comment| class Definition |
         | parent class IRI with the value of PREFIX removed | ParentClassCode |
         | property IRI with the value of PREFIX removed | property Code |
         | property IRI | PropertyUri |
         | property rdfs:comment | property Description |
         | property qudt:hasUnit | property Unit |
         | unique combination of property and class IRIs | OwnedUri |
         | IRI of enumeration property with the value of PREFIX removed | allowed value Code|
         | rdfs:label of enumeration property | allowed value Value |
         | rdfs:comment of enumeration property | allowed value Description |
         | IRI of enumeration property | allowed value OwnedUri |

        Other bSDD values in the target pattern are constant:

         | Constant | bSDD |
         | -------- | ------- |
         | Class | ClassType |
         | EN | CreatorLanguageIsoCode |
         | Active | Status |
         | Property | PropertyType |
        
   
4. Query is sent to the GraphDB repository via REST API
5. HTTP GET Request to buildingSMART bSDD API to retrieve QUDT to bSDD units map is sent.
6. Upon retrieval of class data and unit map data, both datasets are  is post-processed to the format required to prepare bSDD dictionary.
7. Properties data retrieval query is loaded from the filesystem (`./SPARQL/retrieve-properties-info.rq`)
8. Upon retrieval of properties data and unit map data, both datasets are post-processed to the format required to prepare bSDD dictionary. QUDT dimensiton vector URLs are mapped to the bSDD unit format, using the following regular expression: `A([0-9-]+)E([0-9-]+)L([0-9-]+)I([0-9-]+)M([0-9-]+)H([0-9-]+)T([0-9-]+)D([0-9-]+)`

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



Original Tasks description:

- task: https://github.com/statnett/CIM4Enterprise/issues/8 . Convert to BSDD:
  - `Switch, SwitchInfo` and their parent classes (eg `IdentifiedObject, PowerSystemResource, Asset, AssetInfo`)
  - All their properties (data and enum props but not Relations)
  - All their enumerations
- [bsdd-import-model.json](https://raw.githubusercontent.com/buildingSMART/bSDD/refs/heads/master/Model/Import%20Model/bsdd-import-model.json): template JSON for BSDD import
- `bsdd-import-model.yaml`: same but in YAML: easier to edit and allows comments and commenting-out of lines
