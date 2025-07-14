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
Asset.PowerSystemResources
Asset.baselineCondition
Asset.baselineLossOfLife
Asset.lifecycleState
Asset.lotNumber
Asset.position
Asset.purchasePrice
Asset.type
Asset.utcNumber
AssetDeployment.BaseVoltage
AssetDeployment.deploymentState
AssetKind.other
AssetKind.transformer
AssetLifeCycleStateKind.received
AssetModelCatalogueItem
AssetModelCatalogueItem.unitCost
CableInfo
CableInfo.constructionKind
CableInfo.outerJacketKind
CableOuterJacketKind.pvc
CableShieldMaterialKind.aluminum
CableConstructionKind.stranded
Manufacturer
Manufacturer.ProductAssetModel
PowerSystemResource.AssetDatasheet
PowerTransformerInfo
ProductAssetModel
ProductAssetModel.AssetModelCatalogueItem
ProductAssetModel.drawingNumber
ProductAssetModel.instructionMnaual
ProductAssetModel.modelVersion
ProductAssetModel.weightTotal
WireInfo.radius
WireInfo.ratedCurrent
WireInsulationKind.other
WireMaterialKind.aluminum
