# stactools-sentinel5p

- Name: sentinel5p
- Package: `stactools.sentinel5p`
- PypI:
- Owner: @chorng
- Dataset homepage: https://registry.opendata.aws/sentinel5p/
- STAC extensions used:
  - [eo](https://github.com/stac-extensions/eo)
  - [proj](https://github.com/stac-extensions/projection/)
  - [sat](https://github.com/stac-extensions/sat)

This repository will assist you in the generation of STAC files for Sentinel 5P Level 2 products listed below:
- Ultra Violet Aerosol Index (AER_AI)
- Aerosol Layer Height (AER_LH)
- Methane (CH4___)
- Cloud (CLOUD_)
- Carbon Monoxide (CO____)
- Formaldehyde (HCHO__)
- Nitrogen Dioxide (NO2___)
- Ozone Total Column (O3____)
- Ozone Tropospheric Column (O3_TCL)
- Sulphur Dioxide (SO2___)
- NPP-VIIRS Clouds (NP_BD3, NP_BD6, and NP_BD7)

## Examples

### STAC

- [`AER_AI`](examples/S5P_OFFL_L2__AER_AI_20200303T013547_20200303T031717_12367_01_010302_20200306T032414.json)
- [`AER_LH`](examples/S5P_OFFL_L2__AER_LH_20200303T013547_20200303T031717_12367_01_010302_20200306T053814.json)
- [`CH4___`](examples/S5P_OFFL_L2__CH4____20200303T013547_20200303T031717_12367_01_010302_20200306T053811.json)
- [`CLOUD_`](examples/S5P_OFFL_L2__CLOUD__20200303T013547_20200303T031717_12367_01_010107_20200306T032410.json)
- [`CO____`](examples/S5P_OFFL_L2__CO_____20200303T013547_20200303T031717_12367_01_010302_20200306T032410.json)
- [`HCHO__`](examples/S5P_OFFL_L2__HCHO___20200303T013547_20200303T031717_12367_01_010107_20200306T053811.json)
- [`NO2___`](examples/S5P_OFFL_L2__NO2____20200303T013547_20200303T031717_12367_01_010302_20200306T053815.json)
- [`O3____`](examples/S5P_OFFL_L2__O3_____20200303T013547_20200303T031717_12367_01_010107_20200306T053811.json)
- [`O3_TCL`](examples/S5P_OFFL_L2__O3_TCL_20200303T120623_20200309T125248_12373_01_010108_20200318T000106.json)
- [`SO2___`](examples/S5P_OFFL_L2__SO2____20200303T013547_20200303T031717_12367_01_010107_20200306T144427.json)
- [`NP_BD3`](examples/S5P_OFFL_L2__NP_BD3_20200303T013547_20200303T031717_12367_01_010002_20200306T032410.json)
- [`NP_BD6`](examples/S5P_OFFL_L2__NP_BD6_20200303T013547_20200303T031717_12367_01_010002_20200306T032654.json)
- [`NP_BD7`](examples/S5P_OFFL_L2__NP_BD7_20200303T013547_20200303T031717_12367_01_010002_20200306T032925.json)

### Command-line usage

Description of the command line functions

```bash
$ stac sentinel5p create-item source destination
```

Use `stac sentinel5p --help` to see all subcommands and options.
