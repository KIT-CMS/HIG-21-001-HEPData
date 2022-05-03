# HIG-21-001-HEPData
Repository to collect helper scripts to create inputs for HEPData of HIG-21-001 analysis

## Prerequisites

* ROOT
* python3

## Commands to create 1D limits HEPData


### ggphi with bbphi profiled (Figure 9a)

```bash
./create_1D_limits_yaml.py \
    --inputs data/limits/mssm_ggH_lowonly_cmb.json data/limits/mssm_ggH_highonly_cmb.json \
    --process "Gluon fusion:gg\phi" --type-string '$bb\phi$ profiled' \
    --output-file limit_ggphi.yaml --output-directory submission_preparation
```

### bbphi with ggphi profiled (Figure 9b)

```bash
./create_1D_limits_yaml.py \
    --inputs data/limits/mssm_bbH_lowonly_cmb.json data/limits/mssm_bbH_highonly_cmb.json \
    --process "b associated:bb\phi" --type-string '$gg\phi$ profiled' \
    --output-file limit_bbphi.yaml --output-directory submission_preparation
```

### ggphi with bbphi set to 0 (Aux. Figure 37)

```bash
./create_1D_limits_yaml.py \
    --inputs data/limits/mssm_ggH_lowonly_freezebbH_cmb.json data/limits/mssm_ggH_highonly_freezebbH_cmb.json \
    --process "Gluon fusion:gg\phi" --type-string '$bb\phi$ set to zero' \
    --output-file limit_ggphi_freeze_bbphi.yaml --output-directory submission_preparation
```

### bbphi with ggphi set to 0 (Aux. Figure 38)

```bash
./create_1D_limits_yaml.py \
    --inputs data/limits/mssm_bbH_lowonly_freezeggH_cmb.json data/limits/mssm_bbH_highonly_freezeggH_cmb.json \
    --process "b associated:bb\phi" --type-string '$gg\phi$ set to zero' \
    --output-file limit_bbphi_freeze_ggphi.yaml --output-directory submission_preparation
```

### ggphi (t-only) with bbphi profiled (Aux Figure 39)

```bash
./create_1D_limits_yaml.py \
    --inputs data/limits/mssm_ggH_lowonly_Tonly_cmb.json data/limits/mssm_ggH_highonly_Tonly_cmb.json \
    --process "Gluon fusion:gg\phi" --type-string '$bb\phi$ profiled; $gg\phi$ with t quark only' \
    --output-file limit_ggphi_tonly.yaml --output-directory submission_preparation
```

### ggphi (b-only) with bbphi profiled (Aux Figure 40)

```bash
./create_1D_limits_yaml.py \
    --inputs data/limits/mssm_ggH_lowonly_Bonly_cmb.json data/limits/mssm_ggH_highonly_Bonly_cmb.json \
    --process "Gluon fusion:gg\phi" --type-string '$bb\phi$ profiled; $gg\phi$ with b quark only' \
    --output-file limit_ggphi_bonly.yaml --output-directory submission_preparation
```
