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
    --process '$bb\phi$' --type-string '$gg\phi$ set to zero' \
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
    --process '$gg\phi$' --type-string '$bb\phi$ profiled; $gg\phi$ with b quark only' \
    --output-file limit_ggphi_bonly.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity '95% CL limit on $\sigma(gg\phi)B(\phi\rightarrow\tau\tau)$:pb' \
    --additional-qualifiers 'Higgs boson production:Gluon fusion $gg\phi$'
```

### VLQ BM 1 limits (Figure 11a)

```bash
./create_1D_limits_yaml.py \
    --inputs data/vlq_hep_data/limits/vlq_betaRd33_0_grid.json --process '$U_{1}$' \
    --type-string 'VLQ BM 1 interpretation' --output-file limit_vlq_bm1.yaml --output-directory submission_preparation \
    --mass-quantity '$m_U$:TeV' --limit-quantity '95% CL limit on $g_U$:' \
    --additional-qualifiers 'BSM physics:$U_{1}$ t-channel exchange'
```

### VLQ BM 2 limits (Figure 11b)

```bash
./create_1D_limits_yaml.py \
    --inputs data/vlq_hep_data/limits/vlq_betaRd33_minus1_grid.json --process '$U_{1}$' \
    --type-string 'VLQ BM 2 interpretation' --output-file limit_vlq_bm2.yaml --output-directory submission_preparation \
    --mass-quantity '$m_U$:TeV' --limit-quantity '95% CL limit on $g_U$:' \
    --additional-qualifiers 'BSM physics:$U_{1}$ t-channel exchange'
```

### VLQ BM 3 limits (Aux. Figure 92)

```bash
./create_1D_limits_yaml.py \
    --inputs data/vlq_hep_data/limits/vlq_betaRd33_0_offdiag0_grid.json --process '$U_{1}$' \
    --type-string 'VLQ BM 3 interpretation' --output-file limit_vlq_bm3.yaml --output-directory submission_preparation \
    --mass-quantity '$m_U$:TeV' --limit-quantity '95% CL limit on $g_U$:' \
    --additional-qualifiers 'BSM physics:$U_{1}$ t-channel exchange'
```

## Commands to create 1D Significances for HEPData


### ggphi with bbphi profiled (Aux. Figure 31)

```bash
./create_1D_limits_yaml.py \
    --inputs data/pvalues/mssm_ggH_lowonly_pvalue_cmb.json data/pvalues/mssm_ggH_highonly_pvalue_cmb.json \
    --process '$gg\phi$' --type-string '$bb\phi$ profiled' \
    --output-file pvalues_ggphi.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity 'Local significance for a $gg\phi$ signal:' \
    --limit-name-replacement 'Local significance' \
    --additional-qualifiers 'Higgs boson production:Gluon fusion $gg\phi$'
```

### bbphi with ggphi profiled (Aux. Figure 32)

```bash
./create_1D_limits_yaml.py \
    --inputs data/pvalues/mssm_bbH_lowonly_pvalue_cmb.json data/pvalues/mssm_bbH_highonly_pvalue_cmb.json \
    --process '$bb\phi$' --type-string '$gg\phi$ profiled' \
    --output-file pvalues_bbphi.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity 'Local significance for a $bb\phi$ signal:' \
    --limit-name-replacement 'Local significance' \
    --additional-qualifiers 'Higgs boson production:b associated $bb\phi$'
```

### ggphi with bbphi set to 0 (Aux. Figure 33)

```bash
./create_1D_limits_yaml.py \
    --inputs data/pvalues/mssm_ggH_lowonly_freezebbH_pvalue_cmb.json data/pvalues/mssm_ggH_highonly_freezebbH_pvalue_cmb.json \
    --process '$gg\phi$' --type-string '$bb\phi$ set to zero' \
    --output-file pvalues_ggphi_freeze_bbphi.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity 'Local significance for a $gg\phi$ signal:' \
    --limit-name-replacement 'Local significance' \
    --additional-qualifiers 'Higgs boson production:Gluon fusion $gg\phi$'
```

### bbphi with ggphi set to 0 (Aux. Figure 34)

```bash
./create_1D_limits_yaml.py \
    --inputs data/pvalues/mssm_bbH_lowonly_freezeggH_pvalue_cmb.json data/pvalues/mssm_bbH_highonly_freezeggH_pvalue_cmb.json \
    --process '$bb\phi$' --type-string '$gg\phi$ set to zero' \
    --output-file pvalues_bbphi_freeze_ggphi.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity 'Local significance for a bb\phi$ signal:' \
    --limit-name-replacement 'Local significance' \
    --additional-qualifiers 'Higgs boson production:b associated $bb\phi$'
```

### ggphi (t-only) with bbphi profiled (Aux. Figure 35)

```bash
./create_1D_limits_yaml.py \
    --inputs data/pvalues/mssm_ggH_lowonly_Tonly_pvalue_cmb.json data/pvalues/mssm_ggH_highonly_Tonly_pvalue_cmb.json \
    --process '$gg\phi$' --type-string '$bb\phi$ profiled; $gg\phi$ with t quark only' \
    --output-file pvalues_ggphi_tonly.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity 'Local significance for a $gg\phi$ signal:' \
    --limit-name-replacement 'Local significance' \
    --additional-qualifiers 'Higgs boson production:Gluon fusion $gg\phi$'
```

### ggphi (b-only) with bbphi profiled (Aux. Figure 36)

```bash
./create_1D_limits_yaml.py \
    --inputs data/pvalues/mssm_ggH_lowonly_Bonly_pvalue_cmb.json data/pvalues/mssm_ggH_highonly_Bonly_pvalue_cmb.json \
    --process '$gg\phi$' --type-string '$bb\phi$ profiled; $gg\phi$ with b quark only' \
    --output-file pvalues_ggphi_bonly.yaml --output-directory submission_preparation \
    --mass-quantity '$m_\phi$:GeV' --limit-quantity 'Local significance for a $gg\phi$ signal:' \
    --limit-name-replacement 'Local significance' \
    --additional-qualifiers 'Higgs boson production:Gluon fusion $gg\phi$'
```

## Commands to create 2D Likelihood scans HEPData

### Yt-Yb scans for A
```bash
for m in 60 80 95 100 120 125 130 140 160 180 200;
do
    ./create_2D_scans_yaml.py \
        --input data/ys_scans/higgsCombine.Yt_A_vs_Yb_A.MultiDimFit.mH${m}.fixed.root \
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
        --input data/ys_scans/higgsCombine.Yt_H_vs_Yb_H.MultiDimFit.mH${m}.fixed.root \
        --output-file 2D_scan_Yt_Yb_H_m${m}.yaml --output-directory submission_preparation \
        --mass-hypothesis ${m} --x-quantity 'Yt_H:$g_{t}^{H}\sqrt{B(H\rightarrow\tau\tau)}$:' \
        --y-quantity 'Yb_H:$g_{b}^{H}\sqrt{B(H\rightarrow\tau\tau)}$:' --upper-value 1000
done
```

### ggphi-qqphi scans
```bash
./create_2D_scans_yaml.py  \
    --input data/qqh_2d/higgsCombine.r_ggH_vs_r_qqH.MultiDimFit.mH95.fixed.root \
    --output-file 2D_scan_ggphi_qqphi_m95.yaml --output-directory submission_preparation \
    --mass-hypothesis 95 --x-quantity 'r_ggH:$\sigma(gg\phi)B(\phi\rightarrow\tau\tau)$:pb' \
    --y-quantity 'r_qqX:$\sigma(qq\phi)B(\phi\rightarrow\tau\tau)$:pb' --upper-value 1000
```

### ggphi-bbphi scans with real data
```bash
for m in 60 80 95 100 120 125 130 140 160 180 200 250 300 350 400 450 500 600 700 800 900 1000 1200 1400 1600 1800 2000 2300 2600 2900 3200 3500;
do
    ./create_2D_scans_yaml.py \
        --input data/ggH-bbH-scans/scan_values_mH${m}.root \
        --output-file 2D_scan_ggphi_bbphi_m${m}.yaml  --output-directory submission_preparation \
        --mass-hypothesis ${m} --x-quantity 'r_ggH:$\sigma(gg\phi)B(\phi\rightarrow\tau\tau)$:pb' \
        --y-quantity 'r_bbH:$\sigma(bb\phi)B(\phi\rightarrow\tau\tau)$:pb' --upper-value 1000
done
```

### ggphi-bbphi scans with Asimov pseudodata
```bash
for m in 60 80 95 100 120 125 130 140 160 180 200 250 300 350 400 450 500 600 700 800 900 1000 1200 1400 1600 1800 2000 2300 2600 2900 3200 3500;
do
    ./create_2D_scans_yaml.py \
        --input data/ggH-bbH-scans_Asimov/scan_values_mH${m}.root \
        --output-file 2D_scan_ggphi_bbphi_m${m}_Asimov.yaml  --output-directory submission_preparation \
        --mass-hypothesis ${m} --x-quantity 'r_ggH:$\sigma(gg\phi)B(\phi\rightarrow\tau\tau)$:pb' \
        --y-quantity 'r_bbH:$\sigma(bb\phi)B(\phi\rightarrow\tau\tau)$:pb' --upper-value 1000
done
```

## Commands for VLQ 1D Likelihood scans HEPData

### VLQ BM 1 scans

```bash
for m in 1 2 3 4 5;
do
    ./create_1D_vlq_scans_yaml.py \
        --inputs "data/vlq_hep_data/scans_v4/vlq_scan_betaRd33_0_mU${m}000_combined.json:Combined" \
                 "data/vlq_hep_data/scans_v4/vlq_scan_betaRd33_0_mU${m}000_nobtag.json:No b tag" \
                 "data/vlq_hep_data/scans_v4/vlq_scan_betaRd33_0_mU${m}000_btag.json:b tag" \
        --output-file vlq_1D_scan_bm1_mU${m}.yaml --output-directory submission_preparation \
        --additional-qualifiers 'BSM physics:VLQ BM 1 interpretation' \
        --mass-hypothesis ${m} --x-quantity '$g_U$:'
done
```

### VLQ BM 2 scans

```bash
for m in 1 2 3 4 5;
do
    ./create_1D_vlq_scans_yaml.py \
        --inputs "data/vlq_hep_data/scans_v4/vlq_scan_betaRd33_minus1_mU${m}000_combined.json:Combined" \
                 "data/vlq_hep_data/scans_v4/vlq_scan_betaRd33_minus1_mU${m}000_nobtag.json:No b tag" \
                 "data/vlq_hep_data/scans_v4/vlq_scan_betaRd33_minus1_mU${m}000_btag.json:b tag" \
        --output-file vlq_1D_scan_bm2_mU${m}.yaml --output-directory submission_preparation \
        --additional-qualifiers 'BSM physics:VLQ BM 2 interpretation' \
        --mass-hypothesis ${m} --x-quantity '$g_U$:'
done
```

### VLQ BM 3 scans

```bash
for m in 1 2 3 4 5;
do
    ./create_1D_vlq_scans_yaml.py \
        --inputs "data/vlq_hep_data/scans_v4/vlq_scan_betaRd33_0_offdiag0_mU${m}000_combined.json:Combined" \
                 "data/vlq_hep_data/scans_v4/vlq_scan_betaRd33_0_offdiag0_mU${m}000_nobtag.json:No b tag" \
                 "data/vlq_hep_data/scans_v4/vlq_scan_betaRd33_0_offdiag0_mU${m}000_btag.json:b tag" \
        --output-file vlq_1D_scan_bm3_mU${m}.yaml --output-directory submission_preparation \
        --additional-qualifiers 'BSM physics:VLQ BM 3 interpretation' \
        --mass-hypothesis ${m} --x-quantity '$g_U$:'
done
```

## MSSM limits

### mh125 limits (Figure 12a)

```bash
./create_2D_exclusion_contours_yaml.py \
    --input data/model-dependent-limits/asymptotic_grid_2022_04_29_mh125.root \
    --type-string 'MSSM $M_h^{125}$ interpretation' --output-file limit_mssm_mh125.yaml \
    --output-directory submission_preparation \
    --x-quantity '$m_A$:GeV' --y-quantity '$\tan\beta$:'  --min-n-points 10
```

### mh125EFT limits (Figure 12b)

```bash
./create_2D_exclusion_contours_yaml.py \
    --input data/model-dependent-limits/asymptotic_grid_2022_04_29_mh125EFT.root \
    --type-string 'MSSM $M_{h,\,\text{EFT}}^{125}$ interpretation' --output-file limit_mssm_mh125EFT.yaml \
    --output-directory submission_preparation \
    --x-quantity '$m_A$:GeV' --y-quantity '$\tan\beta$:'  --min-n-points 10
```

### mh125_ls limits (Aux. Figure 114)

```bash
./create_2D_exclusion_contours_yaml.py \
    --input data/model-dependent-limits/asymptotic_grid_2022_07_05_mh125_ls.root \
    --type-string 'MSSM $M_h^{125}(\tilde{\tau})$ interpretation' --output-file limit_mssm_mh125_ls.yaml \
    --output-directory submission_preparation \
    --x-quantity '$m_A$:GeV' --y-quantity '$\tan\beta$:'  --min-n-points 10
```

### mh125_lc limits (Aux. Figure 115)

```bash
./create_2D_exclusion_contours_yaml.py \
    --input data/model-dependent-limits/asymptotic_grid_2022_07_05_mh125_lc.root \
    --type-string 'MSSM $M_h^{125}(\tilde{\chi})$ interpretation' --output-file limit_mssm_mh125_lc.yaml \
    --output-directory submission_preparation \
    --x-quantity '$m_A$:GeV' --y-quantity '$\tan\beta$:'  --min-n-points 10
```

### mh125_muneg_1 limits (Aux. Figure 116)

```bash
./create_2D_exclusion_contours_yaml.py \
    --input data/model-dependent-limits/asymptotic_grid_2022_07_05_mh125_muneg_1.root \
    --type-string 'MSSM $M_h^{125\,\mu_{1}-}$ interpretation' --output-file limit_mssm_mh125_muneg_1.yaml \
    --output-directory submission_preparation \
    --x-quantity '$m_A$:GeV' --y-quantity '$\tan\beta$:'  --min-n-points 10
```

### mh125_muneg_2 limits (Aux. Figure 117)

```bash
./create_2D_exclusion_contours_yaml.py \
    --input data/model-dependent-limits/asymptotic_grid_2022_07_05_mh125_muneg_2.root \
    --type-string 'MSSM $M_h^{125\,\mu_{2}-}$ interpretation' --output-file limit_mssm_mh125_muneg_2.yaml \
    --output-directory submission_preparation \
    --x-quantity '$m_A$:GeV' --y-quantity '$\tan\beta$:'  --min-n-points 10
```

### mh125_muneg_3 limits (Aux. Figure 118)

```bash
./create_2D_exclusion_contours_yaml.py \
    --input data/model-dependent-limits/asymptotic_grid_2022_07_05_mh125_muneg_3.root \
    --type-string 'MSSM $M_h^{125\,\mu_{3}-}$ interpretation' --output-file limit_mssm_mh125_muneg_3.yaml \
    --output-directory submission_preparation \
    --x-quantity '$m_A$:GeV' --y-quantity '$\tan\beta$:'  --min-n-points 10
```

### mh1125_CPV limits (Aux. Figure 119)

```bash
./create_2D_exclusion_contours_yaml.py \
    --input data/model-dependent-limits/asymptotic_grid_2022_07_05_mh1125_CPV.root \
    --type-string 'MSSM $M_{h_{1}}^{125}(CPV)$ interpretation' --output-file limit_mssm_mh1125_CPV.yaml \
    --output-directory submission_preparation \
    --x-quantity '$m_{H^{+}}$:GeV' --y-quantity '$\tan\beta$:'  --min-n-points 10
```

### hMSSM limits (Aux. Figure 120)

```bash
./create_2D_exclusion_contours_yaml.py \
    --input data/model-dependent-limits/asymptotic_grid_2022_07_05_hMSSM.root \
    --type-string 'hMSSM interpretation' --output-file limit_mssm_hMSSM.yaml \
    --output-directory submission_preparation \
    --x-quantity '$m_A$:GeV' --y-quantity '$\tan\beta$:'  --min-n-points 10
```

### mHH125 limits (Aux. Figure 121) neglected, since completely excluded

```bash
./create_2D_exclusion_contours_yaml.py \
    --input data/model-dependent-limits/asymptotic_grid_2022_07_05_mHH125.root \
    --type-string 'MSSM $M_H^{125}$ interpretation' --output-file limit_mssm_mHH125.yaml \
    --output-directory submission_preparation \
    --x-quantity '$m_{H^{+}}$:GeV' --y-quantity '$\tan\beta$:'  --min-n-points 10
```

### mh125EFT_lc limits (Aux. Figure 122)

```bash
./create_2D_exclusion_contours_yaml.py \
    --input data/model-dependent-limits/asymptotic_grid_2022_07_05_mh125EFT_lc.root \
    --type-string 'MSSM $M_{h,\,\text{EFT}}^{125}(\tilde{\chi})$ interpretation' --output-file limit_mssm_mh125EFT_lc.yaml \
    --output-directory submission_preparation \
    --x-quantity '$m_A$:GeV' --y-quantity '$\tan\beta$:'  --min-n-points 10
```

### mh125_align limits (Aux. Figure 123)

```bash
./create_2D_exclusion_contours_yaml.py \
    --input data/model-dependent-limits/asymptotic_grid_2022_07_05_mh125_align.root \
    --type-string 'MSSM $M_{h}^{125}(\text{alignment})$ interpretation' --output-file limit_mssm_mh125_align.yaml \
    --output-directory submission_preparation \
    --x-quantity '$m_A$:GeV' --y-quantity '$\tan\beta$:'  --min-n-points 10
```


## Post-fit distributions for all analyses (low- and high-mass)
```bash
./create_postfit_shapes_all_categories.py --n-threads 6 --categories-configurations *categories.yaml
```

## Correlation coefficients of nuisance parameters after a BG only fit

### High-mass analysis
```bash
./create_2D_correlation_yaml.py \
    --input fit_mdf_correlations_highmass.csv --min-correlation 0.011 \
    --output-file  correlations_highmass.yaml --output-directory submission_preparation \
    --additional-qualifiers "Maximum likelihood fit:Background only fit in the \"High-mass\" analysis"
```

### Low-mass analysis
```bash
./create_2D_correlation_yaml.py \
    --input fit_mdf_correlations_lowmass.csv --min-correlation 0.011 \
    --output-file  correlations_lowmass.yaml --output-directory submission_preparation \
    --additional-qualifiers "Maximum likelihood fit:Background only fit in the \"Low-mass\" analysis"
```

## SM ggphi fracions

```bash
./create_sm_ggh_fractions_yaml.py \
    --input sm_ggh_fractions.csv \
    --output-file sm_ggh_fractions.yaml --output-directory submission_preparation
```

## Adding images from the paper repo

### Copying from repo

```bash
./copy_commands.sh $HOME/HIG-21-001
```

### Coverting into required pngs

```bash
pushd submission_preparation/;
for f in *.pdf;
do
    pdftoppm -f 1 -l 1 -png ${f} ${f/.pdf/};
    rm ${f};
    convert -trim ${f/.pdf/-1.png} ${f/.pdf/.png};
    rm ${f/.pdf/-1.png};
    convert -thumbnail 200 ${f/.pdf/.png} thumb_${f/.pdf/.png};
done;
popd;
```
