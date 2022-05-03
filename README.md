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
    --process '$gg\phi$' --type-string '$bb\phi$ profiled' \
    --output-file limit_ggphi.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity '95% CL limit on $\sigma(gg\phi)B(\phi\rightarrow\tau\tau)$:pb' \
    --additional-qualifiers 'Higgs boson production:Gluon fusion $gg\phi$'
```

### bbphi with ggphi profiled (Figure 9b)

```bash
./create_1D_limits_yaml.py \
    --inputs data/limits/mssm_bbH_lowonly_cmb.json data/limits/mssm_bbH_highonly_cmb.json \
    --process '$bb\phi$' --type-string '$gg\phi$ profiled' \
    --output-file limit_bbphi.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity '95% CL limit on $\sigma(bb\phi)B(\phi\rightarrow\tau\tau)$:pb' \
    --additional-qualifiers 'Higgs boson production:b associated $bb\phi$'
```

### ggphi with bbphi set to 0 (Aux. Figure 37)

```bash
./create_1D_limits_yaml.py \
    --inputs data/limits/mssm_ggH_lowonly_freezebbH_cmb.json data/limits/mssm_ggH_highonly_freezebbH_cmb.json \
    --process '$gg\phi$' --type-string '$bb\phi$ set to zero' \
    --output-file limit_ggphi_freeze_bbphi.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity '95% CL limit on $\sigma(gg\phi)B(\phi\rightarrow\tau\tau)$:pb' \
    --additional-qualifiers 'Higgs boson production:Gluon fusion $gg\phi$'
```

### bbphi with ggphi set to 0 (Aux. Figure 38)

```bash
./create_1D_limits_yaml.py \
    --inputs data/limits/mssm_bbH_lowonly_freezeggH_cmb.json data/limits/mssm_bbH_highonly_freezeggH_cmb.json \
    --process '$bb\phi$'" --type-string '$gg\phi$ set to zero' \
    --output-file limit_bbphi_freeze_ggphi.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity '95% CL limit on $\sigma(bb\phi)B(\phi\rightarrow\tau\tau)$:pb' \
    --additional-qualifiers 'Higgs boson production:b associated $bb\phi$'
```

### ggphi (t-only) with bbphi profiled (Aux Figure 39)

```bash
./create_1D_limits_yaml.py \
    --inputs data/limits/mssm_ggH_lowonly_Tonly_cmb.json data/limits/mssm_ggH_highonly_Tonly_cmb.json \
    --process '$gg\phi$' --type-string '$bb\phi$ profiled; $gg\phi$ with t quark only' \
    --output-file limit_ggphi_tonly.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity '95% CL limit on $\sigma(gg\phi)B(\phi\rightarrow\tau\tau)$:pb' \
    --additional-qualifiers 'Higgs boson production:Gluon fusion $gg\phi$'
```

### ggphi (b-only) with bbphi profiled (Aux Figure 40)

```bash
./create_1D_limits_yaml.py \
    --inputs data/limits/mssm_ggH_lowonly_Bonly_cmb.json data/limits/mssm_ggH_highonly_Bonly_cmb.json \
    --process '$gg\phi$ --type-string '$bb\phi$ profiled; $gg\phi$ with b quark only' \
    --output-file limit_ggphi_bonly.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity '95% CL limit on $\sigma(gg\phi)B(\phi\rightarrow\tau\tau)$:pb' \
    --additional-qualifiers 'Higgs boson production:Gluon fusion $gg\phi$'
```

## Commands to create 2D Likelihood scans HEPData

### Yt-Yb scans for A
```bash
for m in 60 80 95 100 120 125 130 140 160 180 200;
do
    ./create_2D_scans_yaml.py \
        --input data/ys_scans/higgsCombine.Yt_A_vs_Yb_A.MultiDimFit.mH${m}.root \
        --output-file 2D_scan_Yt_Yb_A_m${m}.yaml --output-directory submission_preparation \
        --mass-hypothesis ${m} --x-quantity 'Yt_A:$g_{t}^{A}\sqrt{B(A\rightarrow\tau\tau)}$:' \
        --y-quantity 'Yb_A:$g_{b}^{A}\sqrt{B(A\rightarrow\tau\tau)}$:' --upper-value 1000
done
```

### Yt-Yb scans for H
```bash
for m in 60 80 95 100 120 125 130 140 160 180 200;
do
    ./create_2D_scans_yaml.py \
        --input data/ys_scans/higgsCombine.Yt_H_vs_Yb_H.MultiDimFit.mH${m}.root \
        --output-file 2D_scan_Yt_Yb_H_m${m}.yaml --output-directory submission_preparation \
        --mass-hypothesis ${m} --x-quantity 'Yt_H:$g_{t}^{H}\sqrt{B(H\rightarrow\tau\tau)}$:' \
        --y-quantity 'Yb_H:$g_{b}^{H}\sqrt{B(H\rightarrow\tau\tau)}$:' --upper-value 1000
done
```

### ggphi-qqphi scans
```bash
./create_2D_scans_yaml.py  \
    --input data/qqh_2d/higgsCombine.r_ggH_vs_r_qqH.MultiDimFit.mH95.root \
    --output-file 2D_scan_ggphi_qqphi_m95.yaml --output-directory submission_preparation \
    --mass-hypothesis 95 --x-quantity 'r_ggH:$\sigma(gg\phi)B(\phi\rightarrow\tau\tau)$:pb' \
    --y-quantity 'r_qqX:\sigma(qq\phi)B(\phi\rightarrow\tau\tau):pb' --upper-value 1000
```
