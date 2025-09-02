#!perl -w
my @terms = map {chomp; $_} <DATA>;
my @files = sort glob("*.ttl");
my %terms; # {$term}{$file}
my %total; # {$file} or {$term} : ok, this is a big hack
for my $term (@terms) {
  my $matches = `grep -c 'cim:$term a ' *.ttl | grep -v :0`;
  for my $match (split/\n/, $matches) {
    # print STDERR "grep -c $term *.ttl !! $match";
    my ($file,$count) = split/:/, $match;
    $terms{$term}{$file} = $count;
    $total{$term} and $total{$term} += $count or $total{$term} = $count;
    $total{$file} and $total{$file} += $count or $total{$file} = $count;
  };
};
print "|term|", join("|",@files), "|TOTAL|\n";
print "|--" x (@files+2), "|\n";
for $term (@terms) {
  print "|", $term;
  for my $file (@files) {
    print "|", $terms{$term}{$file} // " "
  };
  print "|", $total{$term} // " ", "|\n";
};
print "|TOTAL|", join("|", map $total{$_}, @files), "| |\n";

__DATA__
Asset
Asset.AssetContainer
Asset.AssetInfo
Asset.PowerSystemResource
Asset.PowerSystemResources
Asset.ProductAssetModel
Asset.baselineCondition
Asset.baselineLossOfLife
Asset.critical
Asset.inUseDate
Asset.inUseState
Asset.kind
Asset.lifecycleState
Asset.lotNumber
Asset.position
Asset.purchasePrice
Asset.serialNumber
Asset.type
Asset.utcNumber
AssetDeployment.BaseVoltage
AssetDeployment.deploymentState
AssetInfo.ProductAssetModel
AssetKind.other
AssetKind.transformer
AssetLifeCycleStateKind.received
AssetModelCatalogueItem
AssetModelCatalogueItem.unitCost
AssetOwner
BusbarSectionInfo
CableConstructionKind.stranded
CableInfo
CableInfo.constructionKind
CableInfo.outerJacketKind
CableInfo.shieldMaterial
CableOuterJacketKind.pvc
CableShieldMaterialKind.aluminum
Manufacturer
Manufacturer.ProductAssetModel
Measurement.ACDCTerminal
Measurement.Asset
Organisation.city
Organisation.country
Organisation.eMail
Organisation.phone
Organisation.postalCode
Organisation.streetAddress
OverheadWireInfo
Ownership
Ownership.Asset
Ownership.AssetOwner
Ownership.share
PowerSystemResource.AssetDatasheet
PowerTransformerInfo
ProductAssetModel
ProductAssetModel.AssetInfo
ProductAssetModel.AssetModelCatalogueItem
ProductAssetModel.Manufacturer
ProductAssetModel.catalogueNumber
ProductAssetModel.drawingNumber
ProductAssetModel.instructionMnaual
ProductAssetModel.modelNumber
ProductAssetModel.modelVersion
ProductAssetModel.usageKind
ProductAssetModel.weightTotal
ShuntCompensatorInfo
ShuntCompensatorInfo.maxPowerLoss
ShuntCompensatorInfo.ratedCurrent
ShuntCompensatorInfo.ratedReactivePower
ShuntCompensatorInfo.ratedVoltage
SwitchInfo
SwitchInfo.breakingCapacity
SwitchInfo.isSinglePhase
SwitchInfo.isUnganged
SwitchInfo.ratedCurrent
SwitchInfo.ratedVoltage
TapChangerInfo
TapChangerInfo.highStep
TapChangerInfo.lowStep
TapChangerInfo.neutralStep
TapChangerInfo.neutralU
TapChangerInfo.ratedApparentPower
TapChangerInfo.ratedCurrent
TapChangerInfo.ratedVoltage
TapChangerInfo.stepVoltageIncrement
TransformerEndInfo
TransformerEndInfo.TransformerTankInfo
TransformerEndInfo.connectionKind
TransformerEndInfo.endNumber
TransformerEndInfo.phaseAngleClock
TransformerEndInfo.r
TransformerEndInfo.ratedS
TransformerEndInfo.ratedU
TransformerTankInfo
TransformerTankInfo.PowerTransformerInfo
WireInfo.gmr
WireInfo.insulated
WireInfo.insulationMaterial
WireInfo.material
WireInfo.nominalTemperature
WireInfo.rAC25
WireInfo.rAC75
WireInfo.rDC20
WireInfo.radius
WireInfo.ratedCurrent
WireInsulationKind.other
WireMaterialKind.aluminum
