PTEN composite analysis
================
Kenneth Matreyek
6/19/2020

``` r
rm(list = ls())
knitr::opts_chunk$set(echo = TRUE)

set.seed(1234)
if(!require(reshape)){install.packages("reshape")}
```

    ## Loading required package: reshape

``` r
library(reshape)
if(!require(ggrepel)){install.packages("ggrepel")}
```

    ## Loading required package: ggrepel

    ## Loading required package: ggplot2

``` r
library(ggrepel)
if(!require(uwot)){install.packages("uwot")}
```

    ## Loading required package: uwot

    ## Loading required package: Matrix

    ## 
    ## Attaching package: 'Matrix'

    ## The following object is masked from 'package:reshape':
    ## 
    ##     expand

``` r
library(uwot)
if(!require(scales)){install.packages("scales")}
```

    ## Loading required package: scales

``` r
library(scales)
if(!require(MASS)){install.packages("MASS")}
```

    ## Loading required package: MASS

``` r
library(MASS)
if(!requireNamespace("BiocManager", quietly = TRUE)){install.packages("BiocManager")}
if(!require(ggtree)){install.packages(BiocManager::install("ggtree"))}
```

    ## Loading required package: ggtree

    ## Registered S3 method overwritten by 'treeio':
    ##   method     from
    ##   root.phylo ape

    ## ggtree v2.2.1  For help: https://yulab-smu.github.io/treedata-book/
    ## 
    ## If you use ggtree in published research, please cite the most appropriate paper(s):
    ## 
    ## [36m-[39m Guangchuang Yu. Using ggtree to visualize data on tree-like structures. Current Protocols in Bioinformatics, 2020, 69:e96. doi:10.1002/cpbi.96
    ## [36m-[39m Guangchuang Yu, Tommy Tsan-Yuk Lam, Huachen Zhu, Yi Guan. Two methods for mapping and visualizing associated data on phylogeny using ggtree. Molecular Biology and Evolution 2018, 35(12):3041-3043. doi:10.1093/molbev/msy194
    ## [36m-[39m Guangchuang Yu, David Smith, Huachen Zhu, Yi Guan, Tommy Tsan-Yuk Lam. ggtree: an R package for visualization and annotation of phylogenetic trees with their covariates and other associated data. Methods in Ecology and Evolution 2017, 8(1):28-36. doi:10.1111/2041-210X.12628

    ## 
    ## Attaching package: 'ggtree'

    ## The following object is masked from 'package:Matrix':
    ## 
    ##     expand

    ## The following object is masked from 'package:reshape':
    ## 
    ##     expand

``` r
library(ggtree)
if(!require(reldist)){install.packages("reldist")}
```

    ## Loading required package: reldist

    ## reldist: Relative Distribution Methods
    ## Version 1.6-6 created on 2016-10-07.
    ## copyright (c) 2003, Mark S. Handcock, University of California-Los Angeles
    ##  For citation information, type citation("reldist").
    ##  Type help(package="reldist") to get started.

``` r
library(reldist)
if(!require(tidyverse)){install.packages("tidyverse")}
```

    ## Loading required package: tidyverse

    ## ── Attaching packages ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── tidyverse 1.3.0 ──

    ## ✓ tibble  3.0.1     ✓ dplyr   1.0.0
    ## ✓ tidyr   1.1.0     ✓ stringr 1.4.0
    ## ✓ readr   1.3.1     ✓ forcats 0.5.0
    ## ✓ purrr   0.3.4

    ## ── Conflicts ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── tidyverse_conflicts() ──
    ## x readr::col_factor() masks scales::col_factor()
    ## x purrr::discard()    masks scales::discard()
    ## x tidyr::expand()     masks ggtree::expand(), Matrix::expand(), reshape::expand()
    ## x dplyr::filter()     masks stats::filter()
    ## x dplyr::lag()        masks stats::lag()
    ## x tidyr::pack()       masks Matrix::pack()
    ## x dplyr::rename()     masks reshape::rename()
    ## x dplyr::select()     masks MASS::select()
    ## x tidyr::unpack()     masks Matrix::unpack()

``` r
library(tidyverse)
if(!require(phytools)){install.packages("phytools")}
```

    ## Loading required package: phytools

    ## Loading required package: ape

    ## 
    ## Attaching package: 'ape'

    ## The following object is masked from 'package:ggtree':
    ## 
    ##     rotate

    ## Loading required package: maps

    ## 
    ## Attaching package: 'maps'

    ## The following object is masked from 'package:purrr':
    ## 
    ##     map

``` r
library(phytools)


theme_new <- theme_set(theme_bw())
theme_new <- theme_update(panel.background = element_blank(),
                          panel.border = element_blank(),
                          panel.grid.major = element_line(colour = "grey95"),
                          panel.grid.minor = element_blank())

to_single_notation <- function(arg1){
  if(toupper(arg1) == "ALA"){return("A")}
  if(toupper(arg1) == "CYS"){return("C")}
  if(toupper(arg1) == "ASP"){return("D")}
  if(toupper(arg1) == "GLU"){return("E")}
  if(toupper(arg1) == "PHE"){return("F")}
  if(toupper(arg1) == "GLY"){return("G")}
  if(toupper(arg1) == "HIS"){return("H")}
  if(toupper(arg1) == "ILE"){return("I")}
  if(toupper(arg1) == "LYS"){return("K")}
  if(toupper(arg1) == "LEU"){return("L")}
  if(toupper(arg1) == "MET"){return("M")}
  if(toupper(arg1) == "ASN"){return("N")}
  if(toupper(arg1) == "PRO"){return("P")}
  if(toupper(arg1) == "GLN"){return("Q")}
  if(toupper(arg1) == "ARG"){return("R")}
  if(toupper(arg1) == "SER"){return("S")}
  if(toupper(arg1) == "THR"){return("T")}
  if(toupper(arg1) == "VAL"){return("V")}
  if(toupper(arg1) == "TRP"){return("W")}
  if(toupper(arg1) == "TYR"){return("Y")}
  if(toupper(arg1) == "TER"){return("X")}
}
```

# This is the scoring portion

``` r
pten_seq <- "MTAIIKEIVSRNKRRYQEDGFDLDLTYIYPNIIAMGFPAERLEGVYRNNIDDVVRFLDSKHKNHYKIYNLCAERHYDTAKFNCRVAQYPFEDHNPPQLELIKPFCEDLDQWLSEDDNHVAAIHCKAGKGRTGVMICAYLLHRGKFLKAQEALDFYGEVRTRDKKGVTIPSQRRYVYYYSYLLKNHLDYRPVALLFHKMMFETIPMFSGGTCNPQFVVCQLKVKIYSSNSGPTRREDKFMYFEFPQPLPVCGDIKVEFFHKQNKMLKKDKMFHFWVNTFFIPGPEETSEKVENGSLCDQEIDSICSIERADNDKEYLVLTLTKNDLDKANKDKANRYFSPNFKVKLYFTKTVEEPSNPEASSSTSVTPDVSDNEPDHYRYSDTTDSDPENEPFDEDQHTQITKV"

map <- read.delim(file = "input_datatables/PTEN_variant_barcode_subassembly.tsv", sep = "\t", header= TRUE, stringsAsFactors = FALSE)

map$aa_pos_1 <- 0
map$aa_pos_2 <- 0
map$aa_pos_3 <- 0
map$aa_pos_4 <- 0
for(x in 1:nrow(map)){
  map$aa_pos_1[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(map$value[x]), " \\(p"))[2],")"))[1]))
  map$aa_pos_2[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(map$value[x]), " \\(p"))[3],")"))[1]))
  map$aa_pos_3[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(map$value[x]), " \\(p"))[4],")"))[1]))
  map$aa_pos_4[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(map$value[x]), " \\(p"))[5],")"))[1]))
}

## Get all unique amino acid change positions from above
map$change1 <- 0
map$change2 <- 0
map$change3 <- 0
for(x in 1:nrow(map)){
  map$change1[x] <- unique(c(map$aa_pos_1[x], map$aa_pos_2[x], map$aa_pos_3[x], map$aa_pos_4[x])[c(map$aa_pos_1[x], map$aa_pos_2[x], map$aa_pos_3[x], map$aa_pos_4[x]) != ""])[1]
  map$change2[x] <- unique(c(map$aa_pos_1[x], map$aa_pos_2[x], map$aa_pos_3[x], map$aa_pos_4[x])[c(map$aa_pos_1[x], map$aa_pos_2[x], map$aa_pos_3[x], map$aa_pos_4[x]) != ""])[2]
  map$change3[x] <- unique(c(map$aa_pos_1[x], map$aa_pos_2[x], map$aa_pos_3[x], map$aa_pos_4[x])[c(map$aa_pos_1[x], map$aa_pos_2[x], map$aa_pos_3[x], map$aa_pos_4[x]) != ""])[3]
  if(is.na(map$change1[x] & !is.na(map$change2[x]))){map$change1[x] <- map$change2[x]}
  if(is.na(map$change2[x] & map$change1[x] & !is.na(map$change3[x]))){map$change1[x] <- map$change3[x]}
}

## Find the number of mutations for each variant
map$mut_number <- 0
for(x in 1:nrow(map)){
  map$mut_number[x] <- 3-sum(is.na(map[x,c("change1","change2","change3")]))
}

##
map_singles <- subset(map, mut_number == 1)
map_wt <- subset(map, value == "_wt" & mut_number == 0)
map_syn <- subset(map, !is.na(value) & value != "_wt" & mut_number == 0)

map_singles$start_aa3 <- "NA"
map_singles$end_aa3 <- "NA"

tempy <- subset(map_singles, aa_pos_1 == 1)

for(x in 1:nrow(map_syn)){
  map_syn$position1[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(map_syn$value[x]), split = "\\(p."))[1],3,
                                                              nchar(unlist(strsplit(x = as.character(map_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  map_syn$position2[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(map_syn$value[x]), split = "\\(p."))[2],3,
                                                              nchar(unlist(strsplit(x = as.character(map_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  map_syn$position3[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(map_syn$value[x]), split = "\\(p."))[3],3,
                                                              nchar(unlist(strsplit(x = as.character(map_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  map_syn$position4[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(map_syn$value[x]), split = "\\(p."))[4],3,
                                                              nchar(unlist(strsplit(x = as.character(map_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  map_syn$change1[x] <- unique(c(map_syn$position1[x], map_syn$position2[x], map_syn$position3[x], map_syn$position4[x])[c(map_syn$position1[x], map_syn$position2[x], map_syn$position3[x], map_syn$position4[x]) != ""])[1]
  map_syn$change2[x] <- unique(c(map_syn$position1[x], map_syn$position2[x], map_syn$position3[x], map_syn$position4[x])[c(map_syn$position1[x], map_syn$position2[x], map_syn$position3[x], map_syn$position4[x]) != ""])[2]
  map_syn$change3[x] <- unique(c(map_syn$position1[x], map_syn$position2[x], map_syn$position3[x], map_syn$position4[x])[c(map_syn$position1[x], map_syn$position2[x], map_syn$position3[x], map_syn$position4[x]) != ""])[3]
  map_syn$start[x] <- substr(pten_seq,map_syn$change1[x],map_syn$change1[x])
  map_syn$end[x] <- map_syn$start[x]
  map_syn$variant[x] <- paste(map_syn$start[x],map_syn$change1[x],map_syn$end[x],sep="")
}

for(x in 1:nrow(map_singles)){
  map_singles$start_aa3[x] <- as.character(gsub("[0-9]","",substr(unlist(strsplit(x = as.character(map_singles$value[x]), split = "\\(p."))[2],1,4)))
  if(map_singles$start_aa3[x] == "=), "){
    map_singles$start_aa3[x] <- as.character(gsub("[0-9]","",substr(unlist(strsplit(x = as.character(map_singles$value[x]), split = "\\(p."))[3],1,4)))
  }
  if(map_singles$start_aa3[x] == "=), "){
    map_singles$start_aa3[x] <- as.character(gsub("[0-9]","",substr(unlist(strsplit(x = as.character(map_singles$value[x]), split = "\\(p."))[4],1,4)))
  }
  map_singles$end_aa3[x] <- substr(unlist(strsplit(x = as.character(map_singles$value[x]), split = ")"))[1],nchar(unlist(strsplit(x = as.character(map_singles$value[x]), split = ")"))[1]) - 2,nchar(unlist(strsplit(x = as.character(map_singles$value[x]), split = ")"))[1]))
  if(map_singles$end_aa3[x] == "p.="){
    map_singles$end_aa3[x] <- substr(unlist(strsplit(x = as.character(map_singles$value[x]), split = ")"))[2],nchar(unlist(strsplit(x = as.character(map_singles$value[x]), split = ")"))[2]) - 2,nchar(unlist(strsplit(x = as.character(map_singles$value[x]), split = ")"))[2]))
  }
  if(map_singles$end_aa3[x] == "p.="){
    map_singles$end_aa3[x] <- substr(unlist(strsplit(x = as.character(map_singles$value[x]), split = ")"))[3],nchar(unlist(strsplit(x = as.character(map_singles$value[x]), split = ")"))[3]) - 2,nchar(unlist(strsplit(x = as.character(map_singles$value[x]), split = ")"))[3]))
  }
}

for(x in 1:nrow(map_singles)){
  map_singles$position[x] <- map_singles$aa_pos_1[x]
  if(map_singles$position[x] == "" | is.na(map_singles$position[x])){
    map_singles$position[x] <- map_singles$aa_pos_2[x]
  }
}

map_singles$start <- "NA"
map_singles$end <- "NA"
map_singles$variant <- "NA"

for(x in 1:nrow(map_singles)){
  map_singles$start[x] <- to_single_notation(map_singles$start_aa3[x])
  map_singles$end[x] <- to_single_notation(map_singles$end_aa3[x])
  map_singles$variant[x] <- paste(map_singles$start[x],map_singles$position[x],map_singles$end[x], sep="")
}

map_nonsense <- subset(map_singles, end == "X")
map_missense <- subset(map_singles, end != "X")

map_syn$position <- map_syn$position1
map_wt$class <- "wt"
map_wt$position <- 0
map_wt$start <- "Z"
map_wt$end <- "Z"
map_syn$class <- "syn"
map_nonsense$class <- "nonsense"
map_missense$class <- "missense"
map_wt$variant <- "wt"

PTEN_library_variant_map <- rbind(map_wt[,c("barcode","variant","position","start","end","class")], map_syn[,c("barcode","variant","position","start","end","class")],map_nonsense[,c("barcode","variant","position","start","end","class")],map_missense[,c("barcode","variant","position","start","end","class")])

write.csv(file = "output_datatables/PTEN_library_variant_map.csv", PTEN_library_variant_map, row.names = FALSE, quote = FALSE)
```

``` r
map_msn <- read.csv(file = "input_datatables/Map_msn.csv", header = T, stringsAsFactors = F)

original <- subset(map_msn, library == "original")
fillin <- subset(map_msn, library == "fillin")

length(unique(original$variant))
```

    ## [1] 5192

``` r
length(unique(fillin$variant))
```

    ## [1] 1255

``` r
original_variants <- data.frame("variant" = unique(original$variant), "library" = "original")
fillin_variants <- data.frame("variant" = unique(fillin$variant), "library" = "fillin")

combined_variants <- merge(original_variants, fillin_variants, by = "variant", all = T)
combined_variants <- combined_variants[!(combined_variants$variant == "wt"),]

combined_variants$library <- "none"
for(x in 1:nrow(combined_variants)){
  if(!is.na(combined_variants$library.x[x]) & is.na(combined_variants$library.y[x])){combined_variants$library[x] <- "original"}
  if(is.na(combined_variants$library.x[x]) & !is.na(combined_variants$library.y[x])){combined_variants$library[x] <- "fillin"}
  if(!is.na(combined_variants$library.x[x]) & !is.na(combined_variants$library.y[x])){combined_variants$library[x] <- "both"}
}

combined_variants$position <- gsub("[A-Z]", "", combined_variants$variant)
combined_variants$start <- substr(gsub("[^A-Z]", "", combined_variants$variant),1,1)
combined_variants$end <- substr(gsub("[^A-Z]", "", combined_variants$variant),2,2)

combined_variants$position <- as.numeric(combined_variants$position)

combined_variants$library <- factor(combined_variants$library, levels = c("fillin","original","both"))
PTEN_library_heatmap <- ggplot() + geom_tile(data = combined_variants, aes(x = position, y = end, fill = library)) + scale_x_continuous(expand = c(0,0)) + scale_fill_manual(values = c("brown3","cornflowerblue","black")) + theme(panel.background = element_rect("grey80"), panel.grid.major = element_blank())
ggsave(fil = "Plots/PTEN_library_heatmap.pdf", PTEN_library_heatmap, height = 3, width = 15)
PTEN_library_heatmap
```

![](PTEN_composite_analysis_files/figure-gfm/Look%20at%20coverage%20of%20my%20original%20and%20fillin%20libraries-1.png)<!-- -->

``` r
combined_variants$count <- 1
combined_variants2 <- combined_variants %>% group_by(position,library) %>% summarize(count = sum(count))
```

    ## `summarise()` regrouping output by 'position' (override with `.groups` argument)

``` r
combined_variants2$library <- factor(combined_variants2$library, levels = c("fillin","original","both"))
PTEN_library_bargraph <- ggplot() + geom_bar(data = combined_variants2, aes(x = position, y = count, fill = library), stat = "identity") + scale_fill_manual(values = c("brown3","cornflowerblue","black")) + scale_x_continuous(expand = c(0,0)) + scale_y_continuous(expand = c(0,0))
ggsave(fil = "plots/PTEN_library_bargraph.pdf", PTEN_library_bargraph, height = 3, width = 15)
PTEN_library_bargraph
```

![](PTEN_composite_analysis_files/figure-gfm/Look%20at%20coverage%20of%20my%20original%20and%20fillin%20libraries-2.png)<!-- -->

``` r
e1s1_1a1 <- read.delim(file = "enrich2_output/Rep1_Bin1_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_1a2 <- read.delim(file = "enrich2_output/Rep1_Bin1_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_1a3 <- read.delim(file = "enrich2_output/Rep1_Bin1_PCR1_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_1a <- merge(e1s1_1a1, e1s1_1a2, by = "X", all = T); e1s1_1a <- merge(e1s1_1a, e1s1_1a3, by = "X", all = T); e1s1_1a[is.na(e1s1_1a)] <- 0
e1s1_1a$count <- rowSums(e1s1_1a[,2:4]); e1s1_1a <- e1s1_1a[,c("X","count")]

e1s1_1b1 <- read.delim(file = "enrich2_output/Rep1_Bin1_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_1b2 <- read.delim(file = "enrich2_output/Rep1_Bin1_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_1b3 <- read.delim(file = "enrich2_output/Rep1_Bin1_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_1b <- merge(e1s1_1b1, e1s1_1b2, by = "X", all = T); e1s1_1b <- merge(e1s1_1b, e1s1_1b3, by = "X", all = T); e1s1_1b[is.na(e1s1_1b)] <- 0
e1s1_1b$count <- rowSums(e1s1_1b[,2:4]); e1s1_1b <- e1s1_1b[,c("X","count")]

e1s1_2a1 <- read.delim(file = "enrich2_output/Rep1_Bin2_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_2a2 <- read.delim(file = "enrich2_output/Rep1_Bin2_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_2a3 <- read.delim(file = "enrich2_output/Rep1_Bin2_PCR1_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_2a <- merge(e1s1_2a1, e1s1_2a2, by = "X", all = T); e1s1_2a <- merge(e1s1_2a, e1s1_2a3, by = "X", all = T); e1s1_2a[is.na(e1s1_2a)] <- 0
e1s1_2a$count <- rowSums(e1s1_2a[,2:4]); e1s1_2a <- e1s1_2a[,c("X","count")]

e1s1_2b1 <- read.delim(file = "enrich2_output/Rep1_Bin2_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_2b2 <- read.delim(file = "enrich2_output/Rep1_Bin2_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_2b3 <- read.delim(file = "enrich2_output/Rep1_Bin2_PCR2_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_2b <- merge(e1s1_2b1, e1s1_2b2, by = "X", all = T); e1s1_2b <- merge(e1s1_2b, e1s1_2b3, by = "X", all = T); e1s1_2b[is.na(e1s1_2b)] <- 0
e1s1_2b$count <- rowSums(e1s1_2b[,2:4]); e1s1_2b <- e1s1_2b[,c("X","count")]

e1s1_3a1 <- read.delim(file = "enrich2_output/Rep1_Bin3_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_3a2 <- read.delim(file = "enrich2_output/Rep1_Bin3_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_3a3 <- read.delim(file = "enrich2_output/Rep1_Bin3_PCR1_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_3a <- merge(e1s1_3a1, e1s1_3a2, by = "X", all = T); e1s1_3a <- merge(e1s1_3a, e1s1_3a3, by = "X", all = T); e1s1_3a[is.na(e1s1_3a)] <- 0
e1s1_3a$count <- rowSums(e1s1_3a[,2:4]); e1s1_3a <- e1s1_3a[,c("X","count")]

e1s1_3b1 <- read.delim(file = "enrich2_output/Rep1_Bin3_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_3b2 <- read.delim(file = "enrich2_output/Rep1_Bin3_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_3b3 <- read.delim(file = "enrich2_output/Rep1_Bin3_PCR2_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_3b <- merge(e1s1_3b1, e1s1_3b2, by = "X", all = T); e1s1_3b <- merge(e1s1_3b, e1s1_3b3, by = "X", all = T); e1s1_3b[is.na(e1s1_3b)] <- 0
e1s1_3b$count <- rowSums(e1s1_3b[,2:4]); e1s1_3b <- e1s1_3b[,c("X","count")]

e1s1_4a1 <- read.delim(file = "enrich2_output/Rep1_Bin4_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_4a2 <- read.delim(file = "enrich2_output/Rep1_Bin4_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_4a3 <- read.delim(file = "enrich2_output/Rep1_Bin4_PCR1_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_4a <- merge(e1s1_4a1, e1s1_4a2, by = "X", all = T); e1s1_4a <- merge(e1s1_4a, e1s1_4a3, by = "X", all = T); e1s1_4a[is.na(e1s1_4a)] <- 0
e1s1_4a$count <- rowSums(e1s1_4a[,2:4]); e1s1_4a <- e1s1_4a[,c("X","count")]

e1s1_4b1 <- read.delim(file = "enrich2_output/Rep1_Bin4_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_4b2 <- read.delim(file = "enrich2_output/Rep1_Bin4_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_4b3 <- read.delim(file = "enrich2_output/Rep1_Bin4_PCR2_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s1_4b <- merge(e1s1_4b1, e1s1_4b2, by = "X", all = T); e1s1_4b <- merge(e1s1_4b, e1s1_4b3, by = "X", all = T); e1s1_4b[is.na(e1s1_4b)] <- 0
e1s1_4b$count <- rowSums(e1s1_4b[,2:4]); e1s1_4b <- e1s1_4b[,c("X","count")]

e1s1 <- merge(e1s1_1a, e1s1_1b, by = "X", all = TRUE)
e1s1 <- merge(e1s1, e1s1_2a, by = "X", all = TRUE)
e1s1 <- merge(e1s1, e1s1_2b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s1, e1s1_2b, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y' are duplicated in the result

``` r
e1s1 <- merge(e1s1, e1s1_3a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s1, e1s1_3a, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y' are duplicated in the result

``` r
e1s1 <- merge(e1s1, e1s1_3b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s1, e1s1_3b, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s1 <- merge(e1s1, e1s1_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s1, e1s1_4a, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s1 <- merge(e1s1, e1s1_4b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s1, e1s1_4b, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y', 'count.x', 'count.y', 'count.x', 'count.y' are duplicated
    ## in the result

``` r
colnames(e1s1) <- c("barcode","b1a","b1b","b2a","b2b","b3a","b3b","b4a","b4b")
e1s1 <- merge(e1s1, PTEN_library_variant_map, by = "barcode", all = FALSE)
e1s1[is.na(e1s1)] <- 0

e1s1 <- e1s1 %>% group_by(variant) %>% summarize(b1a = sum(b1a), b1b = sum(b1b), b2a = sum(b2a), b2b = sum(b2b), b3a = sum(b3a), b3b = sum(b3b), b4a = sum(b4a), b4b = sum(b4b), class = unique(class))
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

``` r
e1s1$b1 <- e1s1$b1a + e1s1$b1b; e1s1$b2 <- e1s1$b2a + e1s1$b2b;e1s1$b3 <- e1s1$b3a + e1s1$b3b; e1s1$b4 <- e1s1$b4a + e1s1$b4b

ggplot() + geom_point(data = e1s1, aes(x = b1a, y = b1b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis

    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s1-1.png)<!-- -->

``` r
ggplot() + geom_point(data = e1s1, aes(x = b2a, y = b2b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis
    
    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s1-2.png)<!-- -->

``` r
ggplot() + geom_point(data = e1s1, aes(x = b3a, y = b3b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis
    
    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s1-3.png)<!-- -->

``` r
ggplot() + geom_point(data = e1s1, aes(x = b4a, y = b4b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis
    
    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s1-4.png)<!-- -->

``` r
e1s1$b1 <- e1s1$b1 / sum(e1s1$b1, na.rm = TRUE)
e1s1$b2 <- e1s1$b2 / sum(e1s1$b2, na.rm = TRUE)
e1s1$b3 <- e1s1$b3 / sum(e1s1$b3, na.rm = TRUE)
e1s1$b4 <- e1s1$b4 / sum(e1s1$b4, na.rm = TRUE)
e1s1$mean_freq <- (e1s1$b1 + e1s1$b2 + e1s1$b3 + e1s1$b4) / 4

frequency_filter <- 1e-5 * 10^(1/4)
e1s1 <- subset(e1s1, mean_freq > 1e-5 * 10^(1/4))
e1s1 <- subset(e1s1, mean_freq != 0)
e1s1$weighted_ave <- (e1s1$b1 * 0 + e1s1$b2 * (1/3) + e1s1$b3 * (2/3) + e1s1$b4) /
  rowSums(e1s1[,c("b1","b2","b3","b4")])

write.csv(file = "output_datatables/e1s1_weighted_ave.csv", e1s1, row.names = FALSE, quote = FALSE)
```

``` r
e1s2_1a1 <- read.delim(file = "enrich2_output/Rep2_Bin1_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_1a2 <- read.delim(file = "enrich2_output/Rep2_Bin1_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_1a3 <- read.delim(file = "enrich2_output/Rep2_Bin1_PCR1_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_1a <- merge(e1s2_1a1, e1s2_1a2, by = "X", all = T); e1s2_1a <- merge(e1s2_1a, e1s2_1a3, by = "X", all = T); e1s2_1a[is.na(e1s2_1a)] <- 0
e1s2_1a$count <- rowSums(e1s2_1a[,2:4]); e1s2_1a <- e1s2_1a[,c("X","count")]

e1s2_1b1 <- read.delim(file = "enrich2_output/Rep2_Bin1_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_1b2 <- read.delim(file = "enrich2_output/Rep2_Bin1_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_1b3 <- read.delim(file = "enrich2_output/Rep2_Bin1_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_1b <- merge(e1s2_1b1, e1s2_1b2, by = "X", all = T); e1s2_1b <- merge(e1s2_1b, e1s2_1b3, by = "X", all = T); e1s2_1b[is.na(e1s2_1b)] <- 0
e1s2_1b$count <- rowSums(e1s2_1b[,2:4]); e1s2_1b <- e1s2_1b[,c("X","count")]

e1s2_2a1 <- read.delim(file = "enrich2_output/Rep2_Bin2_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_2a2 <- read.delim(file = "enrich2_output/Rep2_Bin2_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_2a3 <- read.delim(file = "enrich2_output/Rep2_Bin2_PCR1_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_2a <- merge(e1s2_2a1, e1s2_2a2, by = "X", all = T); e1s2_2a <- merge(e1s2_2a, e1s2_2a3, by = "X", all = T); e1s2_2a[is.na(e1s2_2a)] <- 0
e1s2_2a$count <- rowSums(e1s2_2a[,2:4]); e1s2_2a <- e1s2_2a[,c("X","count")]

e1s2_2b1 <- read.delim(file = "enrich2_output/Rep2_Bin2_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_2b2 <- read.delim(file = "enrich2_output/Rep2_Bin2_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_2b3 <- read.delim(file = "enrich2_output/Rep2_Bin2_PCR2_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_2b <- merge(e1s2_2b1, e1s2_2b2, by = "X", all = T); e1s2_2b <- merge(e1s2_2b, e1s2_2b3, by = "X", all = T); e1s2_2b[is.na(e1s2_2b)] <- 0
e1s2_2b$count <- rowSums(e1s2_2b[,2:4]); e1s2_2b <- e1s2_2b[,c("X","count")]

e1s2_3a1 <- read.delim(file = "enrich2_output/Rep2_Bin3_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_3a2 <- read.delim(file = "enrich2_output/Rep2_Bin3_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_3a3 <- read.delim(file = "enrich2_output/Rep2_Bin3_PCR1_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_3a <- merge(e1s2_3a1, e1s2_3a2, by = "X", all = T); e1s2_3a <- merge(e1s2_3a, e1s2_3a3, by = "X", all = T); e1s2_3a[is.na(e1s2_3a)] <- 0
e1s2_3a$count <- rowSums(e1s2_3a[,2:4]); e1s2_3a <- e1s2_3a[,c("X","count")]

e1s2_3b1 <- read.delim(file = "enrich2_output/Rep2_Bin3_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_3b2 <- read.delim(file = "enrich2_output/Rep2_Bin3_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_3b3 <- read.delim(file = "enrich2_output/Rep2_Bin3_PCR2_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_3b <- merge(e1s2_3b1, e1s2_3b2, by = "X", all = T); e1s2_3b <- merge(e1s2_3b, e1s2_3b3, by = "X", all = T); e1s2_3b[is.na(e1s2_3b)] <- 0
e1s2_3b$count <- rowSums(e1s2_3b[,2:4]); e1s2_3b <- e1s2_3b[,c("X","count")]

e1s2_4a1 <- read.delim(file = "enrich2_output/Rep2_Bin4_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_4a2 <- read.delim(file = "enrich2_output/Rep2_Bin4_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_4a3 <- read.delim(file = "enrich2_output/Rep2_Bin4_PCR1_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_4a <- merge(e1s2_4a1, e1s2_4a2, by = "X", all = T); e1s2_4a <- merge(e1s2_4a, e1s2_4a3, by = "X", all = T); e1s2_4a[is.na(e1s2_4a)] <- 0
e1s2_4a$count <- rowSums(e1s2_4a[,2:4]); e1s2_4a <- e1s2_4a[,c("X","count")]

e1s2_4b1 <- read.delim(file = "enrich2_output/Rep2_Bin4_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_4b2 <- read.delim(file = "enrich2_output/Rep2_Bin4_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_4b3 <- read.delim(file = "enrich2_output/Rep2_Bin4_PCR2_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s2_4b <- merge(e1s2_4b1, e1s2_4b2, by = "X", all = T); e1s2_4b <- merge(e1s2_4b, e1s2_4b3, by = "X", all = T); e1s2_4b[is.na(e1s2_4b)] <- 0
e1s2_4b$count <- rowSums(e1s2_4b[,2:4]); e1s2_4b <- e1s2_4b[,c("X","count")]

e1s2 <- merge(e1s2_1a, e1s2_1b, by = "X", all = TRUE)
e1s2 <- merge(e1s2, e1s2_2a, by = "X", all = TRUE)
e1s2 <- merge(e1s2, e1s2_2b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s2, e1s2_2b, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y' are duplicated in the result

``` r
e1s2 <- merge(e1s2, e1s2_3a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s2, e1s2_3a, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y' are duplicated in the result

``` r
e1s2 <- merge(e1s2, e1s2_3b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s2, e1s2_3b, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s2 <- merge(e1s2, e1s2_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s2, e1s2_4a, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s2 <- merge(e1s2, e1s2_4b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s2, e1s2_4b, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y', 'count.x', 'count.y', 'count.x', 'count.y' are duplicated
    ## in the result

``` r
colnames(e1s2) <- c("barcode","b1a","b1b","b2a","b2b","b3a","b3b","b4a","b4b")
e1s2 <- merge(e1s2, PTEN_library_variant_map, by = "barcode", all = FALSE)
e1s2[is.na(e1s2)] <- 0

e1s2 <- e1s2 %>% group_by(variant) %>% summarize(b1a = sum(b1a), b1b = sum(b1b), b2a = sum(b2a), b2b = sum(b2b), b3a = sum(b3a), b3b = sum(b3b), b4a = sum(b4a), b4b = sum(b4b), class = unique(class))
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

``` r
e1s2$b1 <- e1s2$b1a + e1s2$b1b; e1s2$b2 <- e1s2$b2a + e1s2$b2b;e1s2$b3 <- e1s2$b3a + e1s2$b3b; e1s2$b4 <- e1s2$b4a + e1s2$b4b

ggplot() + geom_point(data = e1s2, aes(x = b1a, y = b1b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis

    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s2-1.png)<!-- -->

``` r
ggplot() + geom_point(data = e1s2, aes(x = b2a, y = b2b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis
    
    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s2-2.png)<!-- -->

``` r
ggplot() + geom_point(data = e1s2, aes(x = b3a, y = b3b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis
    
    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s2-3.png)<!-- -->

``` r
ggplot() + geom_point(data = e1s2, aes(x = b4a, y = b4b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis
    
    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s2-4.png)<!-- -->

``` r
e1s2$b1 <- e1s2$b1 / sum(e1s2$b1, na.rm = TRUE)
e1s2$b2 <- e1s2$b2 / sum(e1s2$b2, na.rm = TRUE)
e1s2$b3 <- e1s2$b3 / sum(e1s2$b3, na.rm = TRUE)
e1s2$b4 <- e1s2$b4 / sum(e1s2$b4, na.rm = TRUE)
e1s2$mean_freq <- (e1s2$b1 + e1s2$b2 + e1s2$b3 + e1s2$b4) / 4
e1s2 <- subset(e1s2, mean_freq > 1e-5 * 10^(1/4))
e1s2 <- subset(e1s2, mean_freq != 0)
e1s2$weighted_ave <- (e1s2$b1 * 0 + e1s2$b2 * (1/3) + e1s2$b3 * (2/3) + e1s2$b4) /
  rowSums(e1s2[,c("b1","b2","b3","b4")])

write.csv(file = "Output_datatables/e1s2_weighted_ave.csv", e1s2, row.names = FALSE, quote = FALSE)
```

``` r
e1s3_1a1 <- read.delim(file = "enrich2_output/Rep3_Bin1_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_1a2 <- read.delim(file = "enrich2_output/Rep3_Bin1_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_1a3 <- read.delim(file = "enrich2_output/Rep3_Bin1_PCR1_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_1a <- merge(e1s3_1a1, e1s3_1a2, by = "X", all = T); e1s3_1a <- merge(e1s3_1a, e1s3_1a3, by = "X", all = T); e1s3_1a[is.na(e1s3_1a)] <- 0
e1s3_1a$count <- rowSums(e1s3_1a[,2:4]); e1s3_1a <- e1s3_1a[,c("X","count")]

e1s3_1b1 <- read.delim(file = "enrich2_output/Rep3_Bin1_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_1b2 <- read.delim(file = "enrich2_output/Rep3_Bin1_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_1b3 <- read.delim(file = "enrich2_output/Rep3_Bin1_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_1b <- merge(e1s3_1b1, e1s3_1b2, by = "X", all = T); e1s3_1b <- merge(e1s3_1b, e1s3_1b3, by = "X", all = T); e1s3_1b[is.na(e1s3_1b)] <- 0
e1s3_1b$count <- rowSums(e1s3_1b[,2:4]); e1s3_1b <- e1s3_1b[,c("X","count")]

e1s3_2a1 <- read.delim(file = "enrich2_output/Rep3_Bin2_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_2a2 <- read.delim(file = "enrich2_output/Rep3_Bin2_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_2a3 <- read.delim(file = "enrich2_output/Rep3_Bin2_PCR1_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_2a <- merge(e1s3_2a1, e1s3_2a2, by = "X", all = T); e1s3_2a <- merge(e1s3_2a, e1s3_2a3, by = "X", all = T); e1s3_2a[is.na(e1s3_2a)] <- 0
e1s3_2a$count <- rowSums(e1s3_2a[,2:4]); e1s3_2a <- e1s3_2a[,c("X","count")]

e1s3_2b1 <- read.delim(file = "enrich2_output/Rep3_Bin2_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_2b2 <- read.delim(file = "enrich2_output/Rep3_Bin2_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_2b3 <- read.delim(file = "enrich2_output/Rep3_Bin2_PCR2_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_2b <- merge(e1s3_2b1, e1s3_2b2, by = "X", all = T); e1s3_2b <- merge(e1s3_2b, e1s3_2b3, by = "X", all = T); e1s3_2b[is.na(e1s3_2b)] <- 0
e1s3_2b$count <- rowSums(e1s3_2b[,2:4]); e1s3_2b <- e1s3_2b[,c("X","count")]

e1s3_3a1 <- read.delim(file = "enrich2_output/Rep3_Bin3_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_3a2 <- read.delim(file = "enrich2_output/Rep3_Bin3_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_3a3 <- read.delim(file = "enrich2_output/Rep3_Bin3_PCR1_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_3a <- merge(e1s3_3a1, e1s3_3a2, by = "X", all = T); e1s3_3a <- merge(e1s3_3a, e1s3_3a3, by = "X", all = T); e1s3_3a[is.na(e1s3_3a)] <- 0
e1s3_3a$count <- rowSums(e1s3_3a[,2:4]); e1s3_3a <- e1s3_3a[,c("X","count")]

e1s3_3b1 <- read.delim(file = "enrich2_output/Rep3_Bin3_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_3b2 <- read.delim(file = "enrich2_output/Rep3_Bin3_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_3b3 <- read.delim(file = "enrich2_output/Rep3_Bin3_PCR2_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_3b <- merge(e1s3_3b1, e1s3_3b2, by = "X", all = T); e1s3_3b <- merge(e1s3_3b, e1s3_3b3, by = "X", all = T); e1s3_3b[is.na(e1s3_3b)] <- 0
e1s3_3b$count <- rowSums(e1s3_3b[,2:4]); e1s3_3b <- e1s3_3b[,c("X","count")]

e1s3_4a1 <- read.delim(file = "enrich2_output/Rep3_Bin4_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_4a2 <- read.delim(file = "enrich2_output/Rep3_Bin4_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_4a3 <- read.delim(file = "enrich2_output/Rep3_Bin4_PCR1_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_4a <- merge(e1s3_4a1, e1s3_4a2, by = "X", all = T); e1s3_4a <- merge(e1s3_4a, e1s3_4a3, by = "X", all = T); e1s3_4a[is.na(e1s3_4a)] <- 0
e1s3_4a$count <- rowSums(e1s3_4a[,2:4]); e1s3_4a <- e1s3_4a[,c("X","count")]

e1s3_4b1 <- read.delim(file = "enrich2_output/Rep3_Bin4_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_4b2 <- read.delim(file = "enrich2_output/Rep3_Bin4_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_4b3 <- read.delim(file = "enrich2_output/Rep3_Bin4_PCR2_Seq3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s3_4b <- merge(e1s3_4b1, e1s3_4b2, by = "X", all = T); e1s3_4b <- merge(e1s3_4b, e1s3_4b3, by = "X", all = T); e1s3_4b[is.na(e1s3_4b)] <- 0
e1s3_4b$count <- rowSums(e1s3_4b[,2:4]); e1s3_4b <- e1s3_4b[,c("X","count")]

e1s3 <- merge(e1s3_1a, e1s3_1b, by = "X", all = TRUE)
e1s3 <- merge(e1s3, e1s3_2a, by = "X", all = TRUE)
e1s3 <- merge(e1s3, e1s3_2b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s3, e1s3_2b, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y' are duplicated in the result

``` r
e1s3 <- merge(e1s3, e1s3_3a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s3, e1s3_3a, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y' are duplicated in the result

``` r
e1s3 <- merge(e1s3, e1s3_3b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s3, e1s3_3b, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s3 <- merge(e1s3, e1s3_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s3, e1s3_4a, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s3 <- merge(e1s3, e1s3_4b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s3, e1s3_4b, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y', 'count.x', 'count.y', 'count.x', 'count.y' are duplicated
    ## in the result

``` r
colnames(e1s3) <- c("barcode","b1a","b1b","b2a","b2b","b3a","b3b","b4a","b4b")
e1s3 <- merge(e1s3, PTEN_library_variant_map, by = "barcode", all = FALSE)
e1s3[is.na(e1s3)] <- 0

e1s3 <- e1s3 %>% group_by(variant) %>% summarize(b1a = sum(b1a), b1b = sum(b1b), b2a = sum(b2a), b2b = sum(b2b), b3a = sum(b3a), b3b = sum(b3b), b4a = sum(b4a), b4b = sum(b4b), class = unique(class))
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

``` r
e1s3$b1 <- e1s3$b1a + e1s3$b1b; e1s3$b2 <- e1s3$b2a + e1s3$b2b;e1s3$b3 <- e1s3$b3a + e1s3$b3b; e1s3$b4 <- e1s3$b4a + e1s3$b4b

ggplot() + geom_point(data = e1s3, aes(x = b1a, y = b1b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis

    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s3-1.png)<!-- -->

``` r
ggplot() + geom_point(data = e1s3, aes(x = b2a, y = b2b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis
    
    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s3-2.png)<!-- -->

``` r
ggplot() + geom_point(data = e1s3, aes(x = b3a, y = b3b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis
    
    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s3-3.png)<!-- -->

``` r
ggplot() + geom_point(data = e1s3, aes(x = b4a, y = b4b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis
    
    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s3-4.png)<!-- -->

``` r
e1s3$b1 <- e1s3$b1 / sum(e1s3$b1, na.rm = TRUE)
e1s3$b2 <- e1s3$b2 / sum(e1s3$b2, na.rm = TRUE)
e1s3$b3 <- e1s3$b3 / sum(e1s3$b3, na.rm = TRUE)
e1s3$b4 <- e1s3$b4 / sum(e1s3$b4, na.rm = TRUE)
e1s3$mean_freq <- (e1s3$b1 + e1s3$b2 + e1s3$b3 + e1s3$b4) / 4
e1s3 <- subset(e1s3, mean_freq > 1e-5 * 10^(1/4))
e1s3 <- subset(e1s3, mean_freq != 0)
e1s3$weighted_ave <- (e1s3$b1 * 0 + e1s3$b2 * (1/3) + e1s3$b3 * (2/3) + e1s3$b4) /
  rowSums(e1s3[,c("b1","b2","b3","b4")])

write.csv(file = "output_datatables/e1s3_weighted_ave.csv", e1s3, row.names = FALSE, quote = FALSE)
```

``` r
e1s4_1a1 <- read.delim(file = "enrich2_output/Rep4_Bin1_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_1a2 <- read.delim(file = "enrich2_output/Rep4_Bin1_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_1a <- merge(e1s4_1a1, e1s4_1a2, by = "X", all = T); e1s4_1a[is.na(e1s4_1a)] <- 0; e1s4_1a$count <- e1s4_1a$count.x + e1s4_1a$count.y; e1s4_1a <- e1s4_1a[,c("X","count")]
e1s4_1b1 <- read.delim(file = "enrich2_output/Rep4_Bin1_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_1b2 <- read.delim(file = "enrich2_output/Rep4_Bin1_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_1b <- merge(e1s4_1b1, e1s4_1b2, by = "X", all = T); e1s4_1b[is.na(e1s4_1b)] <- 0; e1s4_1b$count <- e1s4_1b$count.x + e1s4_1b$count.y; e1s4_1b <- e1s4_1b[,c("X","count")]
e1s4_2a1 <- read.delim(file = "enrich2_output/Rep4_Bin2_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_2a2 <- read.delim(file = "enrich2_output/Rep4_Bin2_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_2a <- merge(e1s4_2a1, e1s4_2a2, by = "X", all = T); e1s4_2a[is.na(e1s4_2a)] <- 0; e1s4_2a$count <- e1s4_2a$count.x + e1s4_2a$count.y; e1s4_2a <- e1s4_2a[,c("X","count")]
e1s4_2b1 <- read.delim(file = "enrich2_output/Rep4_Bin2_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_2b2 <- read.delim(file = "enrich2_output/Rep4_Bin2_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_2b <- merge(e1s4_2b1, e1s4_2b2, by = "X", all = T); e1s4_2b[is.na(e1s4_2b)] <- 0; e1s4_2b$count <- e1s4_2b$count.x + e1s4_2b$count.y; e1s4_2b <- e1s4_2b[,c("X","count")]
e1s4_3a1 <- read.delim(file = "enrich2_output/Rep4_Bin3_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_3a2 <- read.delim(file = "enrich2_output/Rep4_Bin3_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_3a <- merge(e1s4_3a1, e1s4_3a2, by = "X", all = T); e1s4_3a[is.na(e1s4_3a)] <- 0; e1s4_3a$count <- e1s4_3a$count.x + e1s4_3a$count.y; e1s4_3a <- e1s4_3a[,c("X","count")]
e1s4_3b1 <- read.delim(file = "enrich2_output/Rep4_Bin3_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_3b2 <- read.delim(file = "enrich2_output/Rep4_Bin3_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_3b <- merge(e1s4_3b1, e1s4_3b2, by = "X", all = T); e1s4_3b[is.na(e1s4_3b)] <- 0; e1s4_3b$count <- e1s4_3b$count.x + e1s4_3b$count.y; e1s4_3b <- e1s4_3b[,c("X","count")]
e1s4_4a1 <- read.delim(file = "enrich2_output/Rep4_Bin4_PCR1_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_4a2 <- read.delim(file = "enrich2_output/Rep4_Bin4_PCR1_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_4a <- merge(e1s4_4a1, e1s4_4a2, by = "X", all = T); e1s4_4a[is.na(e1s4_4a)] <- 0; e1s4_4a$count <- e1s4_4a$count.x + e1s4_4a$count.y; e1s4_4a <- e1s4_4a[,c("X","count")]
e1s4_4b1 <- read.delim(file = "enrich2_output/Rep4_Bin4_PCR2_Seq1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_4b2 <- read.delim(file = "enrich2_output/Rep4_Bin4_PCR2_Seq2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e1s4_4b <- merge(e1s4_4b1, e1s4_4b2, by = "X", all = T); e1s4_4b[is.na(e1s4_4b)] <- 0; e1s4_4b$count <- e1s4_4b$count.x + e1s4_4b$count.y; e1s4_4b <- e1s4_4b[,c("X","count")]

e1s4 <- merge(e1s4_1a, e1s4_1b, by = "X", all = TRUE)
e1s4 <- merge(e1s4, e1s4_2a, by = "X", all = TRUE)
e1s4 <- merge(e1s4, e1s4_2b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s4, e1s4_2b, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y' are duplicated in the result

``` r
e1s4 <- merge(e1s4, e1s4_3a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s4, e1s4_3a, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y' are duplicated in the result

``` r
e1s4 <- merge(e1s4, e1s4_3b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s4, e1s4_3b, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s4 <- merge(e1s4, e1s4_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s4, e1s4_4a, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s4 <- merge(e1s4, e1s4_4b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s4, e1s4_4b, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y', 'count.x', 'count.y', 'count.x', 'count.y' are duplicated
    ## in the result

``` r
colnames(e1s4) <- c("barcode","b1a","b1b","b2a","b2b","b3a","b3b","b4a","b4b")
e1s4 <- merge(e1s4, PTEN_library_variant_map, by = "barcode", all = FALSE)
e1s4[is.na(e1s4)] <- 0

e1s4 <- e1s4 %>% group_by(variant) %>% summarize(b1a = sum(b1a), b1b = sum(b1b), b2a = sum(b2a), b2b = sum(b2b), b3a = sum(b3a), b3b = sum(b3b), b4a = sum(b4a), b4b = sum(b4b), class = unique(class))
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

``` r
e1s4$b1 <- e1s4$b1a + e1s4$b1b; e1s4$b2 <- e1s4$b2a + e1s4$b2b;e1s4$b3 <- e1s4$b3a + e1s4$b3b; e1s4$b4 <- e1s4$b4a + e1s4$b4b

ggplot() + geom_point(data = e1s4, aes(x = b1a, y = b1b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis

    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s4-1.png)<!-- -->

``` r
ggplot() + geom_point(data = e1s4, aes(x = b2a, y = b2b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis
    
    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s4-2.png)<!-- -->

``` r
ggplot() + geom_point(data = e1s4, aes(x = b3a, y = b3b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis
    
    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s4-3.png)<!-- -->

``` r
ggplot() + geom_point(data = e1s4, aes(x = b4a, y = b4b)) + scale_x_log10() + scale_y_log10()
```

    ## Warning: Transformation introduced infinite values in continuous x-axis
    
    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/e1s4-4.png)<!-- -->

``` r
e1s4$b1 <- e1s4$b1 / sum(e1s4$b1, na.rm = TRUE)
e1s4$b2 <- e1s4$b2 / sum(e1s4$b2, na.rm = TRUE)
e1s4$b3 <- e1s4$b3 / sum(e1s4$b3, na.rm = TRUE)
e1s4$b4 <- e1s4$b4 / sum(e1s4$b4, na.rm = TRUE)
e1s4$mean_freq <- (e1s4$b1 + e1s4$b2 + e1s4$b3 + e1s4$b4) / 4
e1s4 <- subset(e1s4, mean_freq > 1e-5 * 10^(1/4))
e1s4 <- subset(e1s4, mean_freq != 0)
e1s4$weighted_ave <- (e1s4$b1 * 0 + e1s4$b2 * (1/3) + e1s4$b3 * (2/3) + e1s4$b4) /
  rowSums(e1s4[,c("b1","b2","b3","b4")])

write.csv(file = "output_datatables/e1s4_weighted_ave.csv", e1s4, row.names = FALSE, quote = FALSE)
```

``` r
e3s1_1a <- read.delim(file = "enrich2_output/Rep5_Bin1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e3s1_2a <- read.delim(file = "enrich2_output/Rep5_Bin2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e3s1_3a <- read.delim(file = "enrich2_output/Rep5_Bin3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e3s1_4a <- read.delim(file = "enrich2_output/Rep5_Bin4.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)

e3s1 <- merge(e3s1_1a, e3s1_2a, by = "X", all = TRUE)
e3s1 <- merge(e3s1, e3s1_3a, by = "X", all = TRUE)
e3s1 <- merge(e3s1, e3s1_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e3s1, e3s1_4a, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y' are duplicated in the result

``` r
colnames(e3s1) <- c("barcode","b1","b2","b3","b4")
e3s1 <- merge(e3s1, PTEN_library_variant_map, by = "barcode", all = FALSE)
e3s1[is.na(e3s1)] <- 0

e3s1 <- e3s1 %>% group_by(variant) %>% summarize(b1 = sum(b1), b2 = sum(b2), b3 = sum(b3), b4 = sum(b4), class = unique(class))
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

``` r
e3s1$b1 <- e3s1$b1 / sum(e3s1$b1, na.rm = TRUE)
e3s1$b2 <- e3s1$b2 / sum(e3s1$b2, na.rm = TRUE)
e3s1$b3 <- e3s1$b3 / sum(e3s1$b3, na.rm = TRUE)
e3s1$b4 <- e3s1$b4 / sum(e3s1$b4, na.rm = TRUE)
e3s1$mean_freq <- (e3s1$b1 + e3s1$b2 + e3s1$b3 + e3s1$b4) / 4
e3s1 <- subset(e3s1, mean_freq > 1e-5 * 10^(1/4))
e3s1 <- subset(e3s1, mean_freq != 0)
e3s1$weighted_ave <- (e3s1$b1 * 0 + e3s1$b2 * (1/3) + e3s1$b3 * (2/3) + e3s1$b4) /
  rowSums(e3s1[,c("b1","b2","b3","b4")])

write.csv(file = "output_datatables/e3s1_weighted_ave.csv", e3s1, row.names = FALSE, quote = FALSE)
```

``` r
e3s2_1a <- read.delim(file = "enrich2_output/Rep6_Bin1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e3s2_2a <- read.delim(file = "enrich2_output/Rep6_Bin2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e3s2_3a <- read.delim(file = "enrich2_output/Rep6_Bin3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e3s2_4a <- read.delim(file = "enrich2_output/Rep6_Bin4.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)

e3s2 <- merge(e3s2_1a, e3s2_2a, by = "X", all = TRUE)
e3s2 <- merge(e3s2, e3s2_3a, by = "X", all = TRUE)
e3s2 <- merge(e3s2, e3s2_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e3s2, e3s2_4a, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y' are duplicated in the result

``` r
colnames(e3s2) <- c("barcode","b1","b2","b3","b4")
e3s2 <- merge(e3s2, PTEN_library_variant_map, by = "barcode", all = FALSE)
e3s2[is.na(e3s2)] <- 0

e3s2 <- e3s2 %>% group_by(variant) %>% summarize(b1 = sum(b1), b2 = sum(b2), b3 = sum(b3), b4 = sum(b4), class = unique(class))
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

``` r
e3s2$b1 <- e3s2$b1 / sum(e3s2$b1, na.rm = TRUE)
e3s2$b2 <- e3s2$b2 / sum(e3s2$b2, na.rm = TRUE)
e3s2$b3 <- e3s2$b3 / sum(e3s2$b3, na.rm = TRUE)
e3s2$b4 <- e3s2$b4 / sum(e3s2$b4, na.rm = TRUE)
e3s2$mean_freq <- (e3s2$b1 + e3s2$b2 + e3s2$b3 + e3s2$b4) / 4
e3s2 <- subset(e3s2, mean_freq > 1e-5 * 10^(1/4))
e3s2 <- subset(e3s2, mean_freq != 0)
e3s2$weighted_ave <- (e3s2$b1 * 0 + e3s2$b2 * (1/3) + e3s2$b3 * (2/3) + e3s2$b4) /
  rowSums(e3s2[,c("b1","b2","b3","b4")])

write.csv(file = "output_datatables/e3s2_weighted_ave.csv", e3s2, row.names = FALSE, quote = FALSE)
```

``` r
e3s3_1a <- read.delim(file = "enrich2_output/Rep7_Bin1.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e3s3_2a <- read.delim(file = "enrich2_output/Rep7_Bin2.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e3s3_3a <- read.delim(file = "enrich2_output/Rep7_Bin3.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
e3s3_4a <- read.delim(file = "enrich2_output/Rep7_Bin4.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)

e3s3 <- merge(e3s3_1a, e3s3_2a, by = "X", all = TRUE)
e3s3 <- merge(e3s3, e3s3_3a, by = "X", all = TRUE)
e3s3 <- merge(e3s3, e3s3_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e3s3, e3s3_4a, by = "X", all = TRUE): column names
    ## 'count.x', 'count.y' are duplicated in the result

``` r
colnames(e3s3) <- c("barcode","b1","b2","b3","b4")
e3s3 <- merge(e3s3, PTEN_library_variant_map, by = "barcode", all = FALSE)
e3s3[is.na(e3s3)] <- 0

e3s3 <- e3s3 %>% group_by(variant) %>% summarize(b1 = sum(b1), b2 = sum(b2), b3 = sum(b3), b4 = sum(b4), class = unique(class))
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

``` r
e3s3$b1 <- e3s3$b1 / sum(e3s3$b1, na.rm = TRUE)
e3s3$b2 <- e3s3$b2 / sum(e3s3$b2, na.rm = TRUE)
e3s3$b3 <- e3s3$b3 / sum(e3s3$b3, na.rm = TRUE)
e3s3$b4 <- e3s3$b4 / sum(e3s3$b4, na.rm = TRUE)
e3s3$mean_freq <- (e3s3$b1 + e3s3$b2 + e3s3$b3 + e3s3$b4) / 4
e3s3 <- subset(e3s3, mean_freq > 1e-5 * 10^(1/4))
e3s3 <- subset(e3s3, mean_freq != 0)
e3s3$weighted_ave <- (e3s3$b1 * 0 + e3s3$b2 * (1/3) + e3s3$b3 * (2/3) + e3s3$b4) /
  rowSums(e3s3[,c("b1","b2","b3","b4")])

write.csv(file = "output_datatables/e3s3_weighted_ave.csv", e3s3, row.names = FALSE, quote = FALSE)
```

``` r
e1s1 <- read.csv(file = "output_datatables/e1s1_weighted_ave.csv", header = T, stringsAsFactors = F)
e1s2 <- read.csv(file = "output_datatables/e1s2_weighted_ave.csv", header = T, stringsAsFactors = F)
e1s3 <- read.csv(file = "output_datatables/e1s3_weighted_ave.csv", header = T, stringsAsFactors = F)
e1s4 <- read.csv(file = "output_datatables/e1s4_weighted_ave.csv", header = T, stringsAsFactors = F)
e3s1 <- read.csv(file = "output_datatables/e3s1_weighted_ave.csv", header = T, stringsAsFactors = F)
e3s2 <- read.csv(file = "output_datatables/e3s2_weighted_ave.csv", header = T, stringsAsFactors = F)
e3s3 <- read.csv(file = "output_datatables/e3s3_weighted_ave.csv", header = T, stringsAsFactors = F)

e1s1$position <- as.numeric(gsub("[A-Z]", "", e1s1$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e1s1$score1 <- (e1s1$weighted_ave - median(subset(e1s1, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e1s1, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e1s1, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))

e1s2$position <- as.numeric(gsub("[A-Z]", "", e1s2$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e1s2$score2 <- (e1s2$weighted_ave - median(subset(e1s2, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e1s2, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e1s2, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))

e1s3$position <- as.numeric(gsub("[A-Z]", "", e1s3$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e1s3$score3 <- (e1s3$weighted_ave - median(subset(e1s3, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e1s3, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e1s3, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))

e1s4$position <- as.numeric(gsub("[A-Z]", "", e1s4$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e1s4$score4 <- (e1s4$weighted_ave - median(subset(e1s4, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e1s4, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e1s4, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))

e3s1$position <- as.numeric(gsub("[A-Z]", "", e3s1$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e3s1$score5 <- (e3s1$weighted_ave - median(subset(e3s1, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e3s1, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e3s1, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))

e3s2$position <- as.numeric(gsub("[A-Z]", "", e3s2$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e3s2$score6 <- (e3s2$weighted_ave - median(subset(e3s2, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e3s2, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e3s2, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))

e3s3$position <- as.numeric(gsub("[A-Z]", "", e3s3$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e3s3$score7 <- (e3s3$weighted_ave - median(subset(e3s3, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e3s3, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e3s3, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))
```

``` r
replicates <- merge(e1s1[,c("variant","score1")], e1s2[,c("variant","score2")], by = "variant", all = TRUE)
replicates <- merge(replicates, e1s3[,c("variant","score3")], by = "variant", all = TRUE)
replicates <- merge(replicates, e1s4[,c("variant","score4")], by = "variant", all = TRUE)
replicates <- merge(replicates, e3s1[,c("variant","score5")], by = "variant", all = TRUE)
replicates <- merge(replicates, e3s2[,c("variant","score6")], by = "variant", all = TRUE)
replicates <- merge(replicates, e3s3[,c("variant","score7")], by = "variant", all = TRUE)

colnames(replicates) <- c("variant","e1s1","e1s2","e1s3","e1s4","e3s1","e3s2","e3s3")
replicates$average <- rowMeans(replicates[,c("e1s1","e1s2","e1s3","e1s4","e3s1","e3s2","e3s3")], na.rm = TRUE)
replicates$count <- rowSums(cbind(!is.na(replicates$e1s1),!is.na(replicates$e1s2),!is.na(replicates$e1s3),!is.na(replicates$e1s4),!is.na(replicates$e3s1),!is.na(replicates$e3s2),!is.na(replicates$e3s3)))

replicates$sd <- rowMeans(cbind(abs(replicates$average-replicates$e1s1), abs(replicates$average-replicates$e1s2)
                                , abs(replicates$average-replicates$e1s3), abs(replicates$average-replicates$e1s4),
                                abs(replicates$average-replicates$e3s1),abs(replicates$average-replicates$e3s2),abs(replicates$average-replicates$e3s3)), na.rm = T)


replicates$class <- "single"
replicates$start <- substr(gsub("[0-9]","",replicates$variant), 1,1)
replicates$end <- substr(gsub("[0-9]","",replicates$variant), 2,2)
replicates$position <- gsub("[^0-9]","",replicates$variant)
replicates[replicates$end == "X","class"] <- "nonsense"
replicates[replicates$class == "single","class"] <- "missense"
replicates[replicates$start == replicates$end,"class"] <- "synonymous"
replicates[replicates$variant == "wt","start"] <- "Z"
replicates[replicates$variant == "wt","position"] <- "0"
replicates[replicates$variant == "wt","end"] <- "Z"

## Let's try to put in some abundance classifications here

replicates$se <- replicates$sd / sqrt(replicates$count)
replicates$lower_ci <- replicates$average - qnorm(0.975) * replicates$se
replicates$upper_ci <- replicates$average + qnorm(0.975) * replicates$se
replicates["average" == "NaN"] <- NA

synonymous_lowest_5percent <- quantile(subset(replicates, class == "synonymous")$average, 0.05, na.rm = TRUE)
synonymous_median <- quantile(subset(replicates, class == "synonymous")$average, 0.5, na.rm = TRUE)
```

``` r
replicate_filter <- 4
passing_replicate_filter <- subset(replicates, count >= replicate_filter)

passing_replicate_filter$abundance_class <- NA
for (x in 1:nrow(passing_replicate_filter)){
  if(is.na(passing_replicate_filter$average[x])){passing_replicate_filter$abundance_class[x] <- "unknown"}
  if(passing_replicate_filter$average[x] < synonymous_lowest_5percent & passing_replicate_filter$upper_ci[x] >= synonymous_lowest_5percent){passing_replicate_filter$abundance_class[x] <- "possibly_low"}
  if(passing_replicate_filter$average[x] < synonymous_lowest_5percent & passing_replicate_filter$upper_ci[x] < synonymous_lowest_5percent){passing_replicate_filter$abundance_class[x] <- "low"}
  if(passing_replicate_filter$average[x] > synonymous_lowest_5percent & passing_replicate_filter$lower_ci[x] < synonymous_lowest_5percent){passing_replicate_filter$abundance_class[x] <- "possibly_wt-like"}
  if(passing_replicate_filter$average[x] > synonymous_lowest_5percent & passing_replicate_filter$lower_ci[x] >= synonymous_lowest_5percent){passing_replicate_filter$abundance_class[x] <- "wt-like"}
}

replicates <- merge(replicates, passing_replicate_filter[,c("variant","abundance_class")], by = "variant", all.x = T)
write.csv(file = "Output_datatables/PTEN_fillin_vampseq_combined.csv", replicates, row.names = FALSE, quote = FALSE)

pten_fillin_vampseq <- ggplot() + 
  geom_density(data = subset(passing_replicate_filter, class == "missense"), aes(x = average), alpha = 0.4) +
  geom_density(data = subset(passing_replicate_filter, class == "nonsense" & (position > 50 | position < 350)), aes(x = average), fill = "blue", alpha = 0.4) +
  geom_density(data = subset(passing_replicate_filter, class == "synonymous"), aes(x = average), fill = "red", alpha = 0.4) +
  geom_vline(xintercept = subset(passing_replicate_filter, variant == "wt")$average)
pten_fillin_vampseq
```

![](PTEN_composite_analysis_files/figure-gfm/Scoring%20things%20with%20a%20replicate%20filter-1.png)<!-- -->

``` r
ggsave(file = "Plots/PTEN_fillin_VAMPseq_densityplot.pdf", pten_fillin_vampseq, height = 3, width = 5)

pten_fillin_vampseq <- ggplot() + 
  geom_histogram(data = subset(passing_replicate_filter, class == "missense"), aes(x = average), alpha = 0.4) +
  geom_histogram(data = subset(passing_replicate_filter, class == "nonsense" & (position > 50 | position < 350)), aes(x = average), fill = "blue", alpha = 0.4) +
  geom_histogram(data = subset(passing_replicate_filter, class == "synonymous"), aes(x = average), fill = "red", alpha = 0.4) +
  geom_vline(xintercept = subset(passing_replicate_filter, variant == "wt")$average)
pten_fillin_vampseq
```

    ## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
    ## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
    ## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.

![](PTEN_composite_analysis_files/figure-gfm/Scoring%20things%20with%20a%20replicate%20filter-2.png)<!-- -->

``` r
ggsave(file = "Plots/PTEN_fillin_VAMPseq_histogram.pdf", pten_fillin_vampseq, height = 3, width = 5)
```

    ## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
    ## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
    ## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.

# This is now the analysis portion

## Import all relevant datasets

``` r
## Import the original dataset with relevant columns
original <- read.delim(file = "input_datatables/PTEN_abundance_original.tsv", header = TRUE, stringsAsFactors = FALSE)
colnames(original)[colnames(original) %in% c("abundance_class","score","sd","expts","se","lower_ci","upper_ci")] <- c("abundance_class_orig","score_orig","sd_orig","count_orig","se_orig","lower_ci_orig","upper_ci_orig")

# Rename the score for the original dataset
colnames(original)[colnames(original) == "score"] <- "score_orig"

## Import the fill-in dataset
replicates <- read.csv(file = "output_datatables/PTEN_fillin_vampseq_combined.csv", header =  TRUE, stringsAsFactors = FALSE)
colnames(replicates)[colnames(replicates) %in% c("e1s1","e1s2","e1s3","e1s4","e3s1","e3s2","e3s3","average","count","sd","se","lower_ci","upper_ci","abundance_class")] <- c("score9","score10","score11","score12","score13","score14","score15","score_fillin","count_fillin","sd_fillin","se_fillin","lower_ci_fillin","upper_ci_fillin","abundance_class_fillin")

combined <- merge(
  replicates[,c("variant","score9","score10","score11","score12","score13","score14","score15","score_fillin","count_fillin","sd_fillin","se_fillin","lower_ci_fillin","upper_ci_fillin","abundance_class_fillin")], 
  original[,c("variant","position","start","end","class","snv","score_orig","abundance_class_orig","sd_orig","count_orig","se_orig","lower_ci_orig","upper_ci_orig","score1","score2","score3","score4","score5","score6","score7","score8")],
  by = "variant", all = T)

combined <- combined[,c("variant","position","start","end","class","snv","score_orig","abundance_class_orig","score_fillin","score1","score2","score3","score4","score5","score6","score7","score8","score9","score10","score11","score12","score13","score14","score15","sd_orig","count_orig","se_orig","lower_ci_orig","upper_ci_orig","sd_fillin","count_fillin","se_fillin","lower_ci_fillin","upper_ci_fillin")]
```

## First paragraph of results

``` r
total_possible <- (402*21) # Includes all missense, nonsense, and synonymous
paste("PTEN variants scored in the first paper:",nrow(subset(combined, !is.na(score_orig)))-2) 
```

    ## [1] "PTEN variants scored in the first paper: 4407"

``` r
paste("PTEN missense variants scored in the first paper:",nrow(subset(combined, class == "missense" & !is.na(score_orig)))-2) 
```

    ## [1] "PTEN missense variants scored in the first paper: 4110"

``` r
paste("Fraction of possible variants scored in the first paper:",round((nrow(subset(combined, !is.na(score_orig)))-2)/total_possible,2))
```

    ## [1] "Fraction of possible variants scored in the first paper: 0.52"

``` r
paste("Number of positions where 18 or more missense variants were scored in the first paper:", sum(data.frame(table((combined %>% filter(class == "missense", !is.na(score_orig) & variant != "M1V"))$position))$Freq >= 18))
```

    ## [1] "Number of positions where 18 or more missense variants were scored in the first paper: 25"

``` r
paste("There were",nrow(subset(replicates, class == "missense")),"unique PTEN missense variants associated with a barcode in the secondary library.")
```

    ## [1] "There were 4186 unique PTEN missense variants associated with a barcode in the secondary library."

## Compare the well-scored variants for the first and second datasets

``` r
combined_5plus <- combined %>% filter(count_orig >= 5 & count_fillin >= 5)

paste("There were",nrow(combined_5plus),"variants that were observed in both experiments in 5 or more replicates, and the there was a Pearson's correlation coefficient (r) of",round(cor(combined_5plus$score_orig, combined_5plus$score_fillin),2),"for the scores of the variants from the two different libraries.")
```

    ## [1] "There were 272 variants that were observed in both experiments in 5 or more replicates, and the there was a Pearson's correlation coefficient (r) of 0.84 for the scores of the variants from the two different libraries."

``` r
lm_orig_fillin <- lm(combined_5plus$score_fillin ~ combined_5plus$score_orig)
paste("For a linear model fit to the overlapping data, the slope was",round(lm_orig_fillin$coefficients[2],2),"and the intercept was",round(lm_orig_fillin$coefficients[1],2))
```

    ## [1] "For a linear model fit to the overlapping data, the slope was 0.89 and the intercept was 0.11"

``` r
Experiment_score_correlation_plot.pdf <- ggplot() + 
  theme_bw() + 
  theme(panel.grid.major = element_blank()) +
  scale_x_continuous(breaks = seq(0,1.2,0.2)) + 
  scale_y_continuous(breaks = seq(0,1.2,0.2)) +
  xlab("Score from original experiment") +
  ylab("Score from second experiment") +
  geom_abline(slope = 1, intercept = 0, alpha = 0.2, size = 10) +
  geom_abline(slope = lm_orig_fillin$coefficients[2], intercept = lm_orig_fillin$coefficients[1], alpha = 0.2, size = 10, color = "blue") +
  geom_point(data = combined_5plus, aes(x = score_orig, y = score_fillin), alpha = 0.5)
Experiment_score_correlation_plot.pdf
```

![](PTEN_composite_analysis_files/figure-gfm/Compare%20between%20the%20two%20datasets-1.png)<!-- -->

``` r
ggsave(file = "plots/Experiment_score_correlation_plot.pdf", Experiment_score_correlation_plot.pdf, height = 80, width = 80, units = "mm")

paste("Pearson's r:",round(cor(combined_5plus$score_orig, combined_5plus$score_fillin, method = "pearson"),2))
```

    ## [1] "Pearson's r: 0.84"

``` r
paste("Percent of variance explained:",round(cor(combined_5plus$score_orig, combined_5plus$score_fillin, method = "pearson")^2,2))
```

    ## [1] "Percent of variance explained: 0.7"

``` r
paste("Percent of variance unexplained:",round(1-cor(combined_5plus$score_orig, combined_5plus$score_fillin)^2,2))
```

    ## [1] "Percent of variance unexplained: 0.3"

# Using all of the available data to ascribe consensus abundance scores

``` r
combined$score_total <- rowMeans(combined[c("score1","score2","score3","score4","score5","score6","score7","score8","score9","score10","score11","score12","score13","score14","score15")], na.rm = T)
combined$count_total <- rowSums(!is.na(combined[c("score1","score2","score3","score4","score5","score6","score7","score8","score9","score10","score11","score12","score13","score14","score15")]))

combined$sd_total <- rowMeans(cbind(abs(combined$score_total-combined$score1), abs(combined$score_total-combined$score2), abs(combined$score_total-combined$score3), abs(combined$score_total-combined$score4), abs(combined$score_total-combined$score5), abs(combined$score_total-combined$score6), abs(combined$score_total-combined$score7), abs(combined$score_total-combined$score8), abs(combined$score_total-combined$score9), abs(combined$score_total-combined$score10), abs(combined$score_total-combined$score11), abs(combined$score_total-combined$score12),abs(combined$score_total-combined$score13),abs(combined$score_total-combined$score14),abs(combined$score_total-combined$score15)), na.rm = T)

combined$se_total <- combined$sd_total / sqrt(combined$count_total)
combined$lower_ci_total <- combined$score_total - qnorm(0.975) * combined$se_total
combined$upper_ci_total <- combined$score_total + qnorm(0.975) * combined$se_total
```

# Creating a schematic that will help in describing hte replicate filtering scheme in a supplementary figure

``` r
schematic_dataframe <- data.frame("variant" = c("A120A","F257F","K322K","A79X","C250X","D331X"),
                                  "class" = c("syn","syn","syn","nonsense","nonsense","nonsense"),
                                  "score" = c(0.8,0.9,0.5,0.1,0.6,0.2),
                                  "linked" = c(7,8,3,4,2,5),
                                  "randomized" = c(2,4,8,5,7,3))

schematic_colorscale <- c("syn" = "red","nonsense" = "blue")

Schematic_1 <- ggplot(data = schematic_dataframe, aes(x = score, fill = class, color = class)) +
  theme(legend.position = "none", panel.grid.major = element_blank(), axis.ticks.y = element_blank(), axis.text.y = element_blank()) +
  xlab("Abundance score") + ylab("Variant count") +
  scale_x_continuous(limits = c(0,1), expand = c(0,0), breaks = c(0,0.5,1)) + scale_y_continuous(expand = c(0,0.1)) +
  scale_fill_manual(values = schematic_colorscale) + scale_color_manual(values = schematic_colorscale) +
  geom_hline(yintercept = 0) + geom_vline(xintercept = 0) +
  geom_point(aes(y = 0), size = 4) +
  geom_density(aes(color = class), alpha = 0.2, adjust = 1.5)
Schematic_1
```

![](PTEN_composite_analysis_files/figure-gfm/Make%20a%20schmatic%20for%20the%20idea%20of%20the%20replicate%20filtering%20scheme-1.png)<!-- -->

``` r
ggsave(file = "Plots/Schematic_1.pdf", Schematic_1, height = 4, width = 6, units = "cm")

Schematic_2 <- ggplot(data = subset(schematic_dataframe, linked >= 4), aes(x = score, fill = class, color = class)) +
  theme(legend.position = "none", panel.grid.major = element_blank(), axis.ticks.y = element_blank(), axis.text.y = element_blank()) +
  xlab("Abundance score") + ylab("Variant count") +
  scale_x_continuous(limits = c(0,1), expand = c(0,0), breaks = c(0,0.5,1)) + scale_y_continuous(expand = c(0,0.1)) +
  scale_fill_manual(values = schematic_colorscale) + scale_color_manual(values = schematic_colorscale) +
  geom_hline(yintercept = 0) + geom_vline(xintercept = 0) +
  geom_point(aes(y = 0), size = 4) +
  geom_density(aes(color = class), alpha = 0.2, adjust = 1.5)
Schematic_2
```

![](PTEN_composite_analysis_files/figure-gfm/Make%20a%20schmatic%20for%20the%20idea%20of%20the%20replicate%20filtering%20scheme-2.png)<!-- -->

``` r
ggsave(file = "Plots/Schematic_2.pdf", Schematic_2, height = 4, width = 6, units = "cm")

Schematic_3 <- ggplot(data = subset(schematic_dataframe, randomized >= 4), aes(x = score, fill = class, color = class)) +
  theme(legend.position = "none", panel.grid.major = element_blank(), axis.ticks.y = element_blank(), axis.text.y = element_blank()) +
  xlab("Abundance score") + ylab("Variant count") +
  scale_x_continuous(limits = c(0,1), expand = c(0,0), breaks = c(0,0.5,1)) + scale_y_continuous(expand = c(0,0.1)) +
  scale_fill_manual(values = schematic_colorscale) + scale_color_manual(values = schematic_colorscale) +
  geom_hline(yintercept = 0) + geom_vline(xintercept = 0) +
  geom_point(aes(y = 0), size = 4) +
  geom_density(aes(color = class), alpha = 0.2, adjust = 1.5)
Schematic_3
```

![](PTEN_composite_analysis_files/figure-gfm/Make%20a%20schmatic%20for%20the%20idea%20of%20the%20replicate%20filtering%20scheme-3.png)<!-- -->

``` r
ggsave(file = "Plots/Schematic_3.pdf", Schematic_3, height = 4, width = 6, units = "cm")
```

# Lets optimize replicate number cutoff based on controls (synonymous and nonsense)

``` r
summary_frame<- data.frame("cutoff_inclusive" = seq(1,15))
resampling_number <-100

for(y in 1:resampling_number){
  observed_frame <- data.frame("cutoff_inclusive" = seq(1,15))
  observed_frame$syn_value <- 0
  observed_frame$called_correctly <- 0
  
  shuffled_frame <- data.frame("cutoff_inclusive" = seq(1,15))
  shuffled_frame$syn_value <- 0
  shuffled_frame$called_correctly <- 0
  
  scorable_syn <- nrow(subset(combined, class == "synonymous" & !is.na(score_total)))
  scorable_syn_subset <- subset(combined, class == "synonymous" & !is.na(score_total))
  scorable_syn_subset$shuffled_score_total <- sample(scorable_syn_subset$score_total, replace = F)
  
  scorable_nonsense <- nrow(subset(combined, class == "nonsense" & !is.na(score_total) & position < 350 & position > 50))
  nonsense_with_scores <- subset(combined, class == "nonsense" & !is.na(score_total))
  nonsense_with_scores$shuffled_upperci <- sample(nonsense_with_scores$upper_ci_total, replace = F)
  
  for(x in 1:nrow(observed_frame)){
    temp_subset <- subset(combined, count_total >= observed_frame$cutoff_inclusive[x] & !is.na(score_total))
    temp_subset_syn <- subset(scorable_syn_subset, class == "synonymous" & count_total >= observed_frame$cutoff_inclusive[x] & !is.na(score_total))
    temp_subset_syn_threshold <- quantile(temp_subset_syn$score_total, 0.05)
    temp_subset_nonsense <- subset(nonsense_with_scores, count_total >= observed_frame$cutoff_inclusive[x] & !is.na(score_total) & position < 350 & position > 50)
    
    called_correctly <- sum(temp_subset_nonsense$upper_ci_total < temp_subset_syn_threshold, na.rm = T)
    called_incorrectly <- sum(temp_subset_nonsense$upper_ci_total >= temp_subset_syn_threshold, na.rm = T)
    observed_frame$syn_value[x] <- temp_subset_syn_threshold
    observed_frame$called_correctly[x] <- called_correctly
    
    temp_subset_syn_threshold_shuffled <- quantile(temp_subset_syn$shuffled_score_total, 0.05)
    random_correctly <- sum(temp_subset_nonsense$shuffled_upperci < temp_subset_syn_threshold_shuffled, na.rm = T)
    random_incorrectly <- sum(temp_subset_nonsense$shuffled_upperci >= temp_subset_syn_threshold_shuffled, na.rm = T)
    shuffled_frame$syn_value[x] <- temp_subset_syn_threshold_shuffled
    shuffled_frame$called_correctly[x] <- random_correctly
  }
  summary_frame <- cbind(summary_frame, observed_frame$called_correctly - shuffled_frame$called_correctly)
}

summary_frame$average_correct <- rowMeans(summary_frame[,seq(2,resampling_number+1)])
summary_frame_melted <- melt(summary_frame[,seq(1,resampling_number+1)], id = "cutoff_inclusive")

replicate_cutoff_nonsense_syn_plot <- ggplot() + 
  theme_bw() + 
  theme(panel.grid.major.x = element_blank()) +
  ylab("Nonsense variants scored over random") +
  geom_jitter(data = summary_frame_melted, aes(x = cutoff_inclusive, y = value), alpha = 0.1, width = 0.2) +
  geom_boxplot(data = summary_frame_melted, aes(x = cutoff_inclusive, y = value, group = cutoff_inclusive), alpha = 0.2, fill = "red")
replicate_cutoff_nonsense_syn_plot
```

![](PTEN_composite_analysis_files/figure-gfm/Optimizing%20replicate%20numbers-1.png)<!-- -->

``` r
ggsave(file = "Plots/Replicate_cutoff_nonsense_syn_plot.pdf", replicate_cutoff_nonsense_syn_plot, height = 60, width = 80, units = "mm")
```

# Using the optimal replicate filter value obtained from the above graph to actually filter the data

``` r
combined$score_abundance <- NA
for(x in 1:nrow(combined)){
  if(combined$count_total[x] >= 4){combined$score_abundance[x] <- combined$score_total[x]}
}

synonymous_lowest_5percent <- quantile(subset(combined, class == "synonymous")$score_abundance, 0.05, na.rm = TRUE)
synonymous_median <- quantile(subset(combined, class == "synonymous")$score_abundance, 0.5, na.rm = TRUE)

combined_for_plotting_classes <- rbind(
  combined %>% filter(class == "missense") %>% mutate(plotting_group = "missense"),
  combined %>% filter(class == "synonymous") %>% mutate(plotting_group = "synonymous"),
  combined %>% filter(class == "nonsense" & position < 350 & position > 50) %>% mutate(plotting_group = "nonsense"))

combined_for_plotting_classes$plotting_group = factor(combined_for_plotting_classes$plotting_group, levels = c("synonymous","nonsense","missense"))

Synonymous_nonsense_missense_histograms_plot <- ggplot() + 
  theme_bw() + 
  theme(panel.grid.major.y = element_blank()) +
  xlab("Abundance score") + 
  geom_hline(yintercept = 0) +
  geom_histogram(data = combined_for_plotting_classes, aes(x = score_abundance), fill = "grey50", alpha = 0.5, color = "black") +
  facet_grid(rows = vars(plotting_group), scales = "free_y")
Synonymous_nonsense_missense_histograms_plot
```

    ## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.

    ## Warning: Removed 3436 rows containing non-finite values (stat_bin).

![](PTEN_composite_analysis_files/figure-gfm/Using%20above%20graph%20make%20the%20right%20dataset-1.png)<!-- -->

``` r
ggsave(file = "Plots/Synonymous_nonsense_missense_histograms_plot.pdf", Synonymous_nonsense_missense_histograms_plot, height = 80, width = 80, units = "mm")
```

    ## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.

    ## Warning: Removed 3436 rows containing non-finite values (stat_bin).

# To validate that the updated dataset is higher in quality, assess how the coefficient of variation changed for variants observed in both datasets

``` r
combined_for_plotting_classes_4plus <- combined_for_plotting_classes %>% filter(count_total >= 4 & count_orig >= 4 & score_orig >= -0.2 & score_total >= -0.2)

combined_for_plotting_classes_4plus$cv_orig <- combined_for_plotting_classes_4plus$sd_orig / combined_for_plotting_classes_4plus$score_orig
combined_for_plotting_classes_4plus$cv_total <- combined_for_plotting_classes_4plus$sd_total / combined_for_plotting_classes_4plus$score_total

combined_for_plotting_classes_4plus[combined_for_plotting_classes_4plus$cv_orig < - 0.1,"cv_orig"] <- -0.2
combined_for_plotting_classes_4plus[combined_for_plotting_classes_4plus$cv_total < - 0.1,"cv_total"] <- -0.2

combined_for_plotting_classes_4plus[combined_for_plotting_classes_4plus$cv_orig > 1.5,"cv_orig"] <- 1.7
combined_for_plotting_classes_4plus[combined_for_plotting_classes_4plus$cv_total > 1.5,"cv_total"] <- 1.7

paste("fraction of original missense variants with CV < 0.5:",round(nrow(subset(combined_for_plotting_classes_4plus, cv_orig > 0 & cv_orig < 0.5)) / nrow(combined_for_plotting_classes_4plus),2))
```

    ## [1] "fraction of original missense variants with CV < 0.5: 0.76"

``` r
paste("fraction of total missense variants with CV < 0.5:",round(nrow(subset(combined_for_plotting_classes_4plus, cv_total > 0 & cv_total < 0.5)) / nrow(combined_for_plotting_classes_4plus),2))
```

    ## [1] "fraction of total missense variants with CV < 0.5: 0.8"

``` r
paste("fraction of original missense variants with CV > 1.5:",round(nrow(subset(combined_for_plotting_classes_4plus, cv_orig > 0 & cv_orig > 1.5)) / nrow(combined_for_plotting_classes_4plus),2))
```

    ## [1] "fraction of original missense variants with CV > 1.5: 0.02"

``` r
paste("fraction of total missense variants with CV > 1.5:",round(nrow(subset(combined_for_plotting_classes_4plus, cv_total > 0 & cv_total > 1.5)) / nrow(combined_for_plotting_classes_4plus),2))
```

    ## [1] "fraction of total missense variants with CV > 1.5: 0.01"

``` r
Coefficient_of_variation_plot <- 
ggplot() + theme_bw() + 
  scale_x_continuous(limits = c(-0.25,1.8)) +
  geom_histogram(data = combined_for_plotting_classes_4plus, aes(x = cv_orig), fill = "blue", alpha = 0.5, color = "blue", binwidth = 0.05) +
  geom_histogram(data = combined_for_plotting_classes_4plus, aes(x = cv_total), fill = "red", alpha = 0.5, color = "red", binwidth = 0.05) +
  geom_vline(xintercept = 0.5, linetype = 2, alpha = 0.4) + geom_vline(xintercept = 0, linetype = 2, alpha = 0.4) +
  ylab("Number of variants") + xlab("Coefficient of variation")
Coefficient_of_variation_plot
```

    ## Warning: Removed 2 rows containing missing values (geom_bar).
    
    ## Warning: Removed 2 rows containing missing values (geom_bar).

![](PTEN_composite_analysis_files/figure-gfm/Compare%20CV%20for%20variants%20we%20had%20seen%20before-1.png)<!-- -->

``` r
ggsave(file = "Plots/Coefficient_of_variation_plot.pdf", Coefficient_of_variation_plot, height = 40, width = 80, units = "mm")
```

    ## Warning: Removed 2 rows containing missing values (geom_bar).
    
    ## Warning: Removed 2 rows containing missing values (geom_bar).

## Ascribe abundance classes based on the full dataset

``` r
synonymous_lowest_5percent <- quantile(subset(combined, class == "synonymous")$score_abundance, 0.05, na.rm = TRUE)
synonymous_median <- quantile(subset(combined, class == "synonymous")$score_abundance, 0.5, na.rm = TRUE)

combined$abundance_class <- NA
for (x in 1:nrow(combined)){
  if(is.na(combined$score_abundance[x]) | is.na(combined$upper_ci_total[x]) | is.na(combined$lower_ci_total[x])){combined$abundance_class[x] <- "unknown"} else{
    if(combined$score_abundance[x] < synonymous_lowest_5percent){combined$abundance_class[x] <- "possibly_low"}
    if(combined$upper_ci_total[x] < synonymous_lowest_5percent){combined$abundance_class[x] <- "low"}
    if(combined$score_abundance[x] > synonymous_lowest_5percent){combined$abundance_class[x] <- "possibly_wt-like"}
    if(combined$lower_ci_total[x] > synonymous_lowest_5percent){combined$abundance_class[x] <- "wt-like"}
  }
}

## Export the initial data
PTEN_abundance_table <- subset(combined, abundance_class %in% c("low","possibly_low","wt-like","possibly_wt-like"))[,c("variant","position","start","end","abundance_class")]
PTEN_abundance_table$position <- as.numeric(PTEN_abundance_table$position)
PTEN_abundance_table <- PTEN_abundance_table[order(PTEN_abundance_table$position),]

write.csv(file = "output_datatables/PTEN_abundance_table.csv", row.names = F, PTEN_abundance_table, quote = F)
```

# A summary of key stats from the composite abundance dataset

``` r
paste("Number of variants that were not scored before but now have scores",nrow(combined %>% filter(is.na(score_orig) & !is.na(score_abundance))))
```

    ## [1] "Number of variants that were not scored before but now have scores 765"

``` r
paste("Number of variants that were originally scored but given new data with the fill-in experiments:",nrow(combined %>% filter(!is.na(score_orig)) %>% filter((is.na(score9) & is.na(score10) & is.na(score11) & is.na(score12) & is.na(score13) & is.na(score14) & is.na(score15))) %>% filter(count_total >= 4)))
```

    ## [1] "Number of variants that were originally scored but given new data with the fill-in experiments: 607"

``` r
paste("Number of total PTEN variants currently scored:",round(nrow(subset(combined, !is.na(score_abundance))),2))
```

    ## [1] "Number of total PTEN variants currently scored: 4723"

``` r
paste("Number of missense PTEN variants currently scored:",round(nrow(subset(combined, !is.na(score_abundance) & class == "missense")),2))
```

    ## [1] "Number of missense PTEN variants currently scored: 4387"

``` r
paste("Number of nonsense PTEN variants currently scored:",round(nrow(subset(combined, !is.na(score_abundance) & class == "nonsense")),2))
```

    ## [1] "Number of nonsense PTEN variants currently scored: 160"

``` r
paste("Number of synonymous PTEN variants currently scored:",round(nrow(subset(combined, !is.na(score_abundance) & class == "synonymous")),2))
```

    ## [1] "Number of synonymous PTEN variants currently scored: 144"

``` r
paste("Number of low abundance PTEN variants intepreted in total:",round(nrow(subset(combined, abundance_class %in% c("low"))),2))
```

    ## [1] "Number of low abundance PTEN variants intepreted in total: 1423"

``` r
paste("Number of WT-like abundance PTEN variants intepreted in total:",round(nrow(subset(combined, abundance_class %in% c("wt-like"))),2))
```

    ## [1] "Number of WT-like abundance PTEN variants intepreted in total: 1740"

``` r
paste("The number of additional low abundance variants identified in the combined dataset:",nrow(subset(combined, abundance_class %in% c("low"))) - nrow(subset(combined, abundance_class_orig %in% c("low"))))
```

    ## [1] "The number of additional low abundance variants identified in the combined dataset: 163"

``` r
paste("The number of additional WT-like abundance variants identified in the combined dataset:",nrow(subset(combined, abundance_class %in% c("wt-like"))) - nrow(subset(combined, abundance_class_orig %in% c("wt-like"))))
```

    ## [1] "The number of additional WT-like abundance variants identified in the combined dataset: 162"

``` r
interpreted_subset <- subset(combined, abundance_class %in% c("low","wt-like"))
paste("Fraction of scored variants in the combined study considered low or WT-like:",round(nrow(subset(combined, abundance_class %in% c("low","wt-like"))) / nrow(subset(combined, abundance_class %in% c("low","wt-like","possibly_low","possibly_wt-like"))),2))
```

    ## [1] "Fraction of scored variants in the combined study considered low or WT-like: 0.67"

``` r
paste("Fraction of scored variants in the original study considered low or WT-like:",round(nrow(subset(combined, abundance_class_orig %in% c("low","wt-like")))/nrow(subset(combined, abundance_class_orig %in% c("low","wt-like","possibly_low","possibly_wt-like"))),2))
```

    ## [1] "Fraction of scored variants in the original study considered low or WT-like: 0.64"

## Mighell et al recently imputed some of the missing scores in the initial abundance dataset. See how their imputated values correlated with the actual values we got once we performed the fill-in experiment.

``` r
mighell <- read.csv(file = "input_datatables/Mighell_imputed_abundance.csv")
colnames(mighell)[1] <- "variant"

combined_only_second_library <- combined %>% filter(is.na(score_orig) & !is.na(score_abundance))
combined_only_second_library2 <- merge(combined_only_second_library, mighell[,c("variant","abundance_score")], by = "variant")

paste("The Pearson's r for the scored and imputed data is:", round(cor(combined_only_second_library2$score_abundance, combined_only_second_library2$abundance_score, method = "pearson"),2))
```

    ## [1] "The Pearson's r for the scored and imputed data is: 0.73"

``` r
real_vs_imputed_plot <- ggplot() + 
  theme_bw() + 
  labs(x = "Abundance score from fillin library", y = "Imputed score by Mighell 2020") +
  scale_x_continuous(limits = c(0,1.2)) + scale_y_continuous(limits = c(0,1.2)) +
  geom_point(data = combined_only_second_library2, aes(x = score_abundance, y = abundance_score), alpha = 0.4)
real_vs_imputed_plot
```

    ## Warning: Removed 15 rows containing missing values (geom_point).

![](PTEN_composite_analysis_files/figure-gfm/Compare%20Mighell%202020%20imputed%20data-1.png)<!-- -->

``` r
ggsave(file = "plots/Abundance_real_vs_imputed_plot.pdf", height = 4, width = 4)
```

    ## Warning: Removed 15 rows containing missing values (geom_point).

# Updating the ClinVar assessments with the composite abundance dataset

#### Bringing in a more recent PTEN ClinVar dataset

``` r
## Add annotations for Clinvar
clinvar <- read.table(file = "input_datatables/191016_PTEN_clinvar_missense_nonsense.tsv", header = TRUE, sep = "\t")
clinvar$Name <- as.character(clinvar$Name)
clinvar$position <- substr(clinvar$Name, nchar((clinvar$Name)) - 12, nchar((clinvar$Name)))
clinvar <- clinvar[grepl("\\(p.", clinvar$position),]
for (x in 1:nrow(clinvar)){clinvar$position[x] <- unlist(strsplit(clinvar$position[x],"\\(p."))[2]}
clinvar <- subset(clinvar, position != "")
clinvar <- subset(clinvar, nchar(position) < 20)
clinvar$start <- "NA"
clinvar$end <- "NA"
for (x in 1:nrow(clinvar)){
  clinvar$start[x] <- substr(clinvar$position[x], 1, 3)
  clinvar$end[x] <- substr(clinvar$position[x], nchar(toString(clinvar$position[x]))-4, nchar(toString(clinvar$position[x])))}
clinvar$start <- gsub("[^A-Za-z]", "", clinvar$start)
clinvar$end <- gsub("[^A-Za-z]", "", clinvar$end)
clinvar$position <- gsub("[^0-9]", "", clinvar$position)
for (x in 1:nrow(clinvar)){
  clinvar$start[x] <- to_single_notation(clinvar$start[x])
  clinvar$end[x] <- to_single_notation(clinvar$end[x])
}
clinvar$variant <- paste(clinvar$start, clinvar$position, clinvar$end, sep ="")
clinvar2 <- clinvar[c("variant","Condition.s.","Clinical.significance..Last.reviewed.")]
colnames(clinvar2) <- c("variant","clinvar_disease","clinvar_interpretation")

clinvar2$clinvar_pathog <- 0
clinvar2$clinvar_likely_pathog <- 0
clinvar2$clinvar_uncertain <- 0
clinvar2$clinvar_likely_benign <- 0
clinvar2$clinvar_benign <- 0

for(x in 1:nrow(clinvar2)){
  if(grepl("Pathogenic",clinvar2$clinvar_interpretation[x]) == TRUE){
    clinvar2$clinvar_pathog[x] <- 1}
  if(grepl("Likely pathogenic",clinvar2$clinvar_interpretation[x]) == TRUE){
    clinvar2$clinvar_likely_pathog[x] <- 1}
  if(grepl("Uncertain",clinvar2$clinvar_interpretation[x]) == TRUE){
    clinvar2$clinvar_uncertain[x] <- 1}
  if(grepl("Conflicting",clinvar2$clinvar_interpretation[x]) == TRUE){
    clinvar2$clinvar_uncertain[x] <- 1}
  if(grepl("Likely benign",clinvar2$clinvar_interpretation[x]) == TRUE){
    clinvar2$clinvar_likely_benign[x] <- 1}
  if(grepl("Benign",clinvar2$clinvar_interpretation[x]) == TRUE){
    clinvar2$clinvar_benign[x] <- 1}
}

## Manually fixing PTEN LP/P CLinVar conflicts / double-counts
pten_lp_p_conflicts <- clinvar2[grep("Pathogenic/Likely pathogenic",clinvar2$clinvar_interpretation),]
clinvar2[clinvar2$variant == "H61R","clinvar_likely_pathog"] <- 0 ## The 2017 Pathogenic Assertion by Herman Laboratory,Nationwide Children's Hospital is much better supported
clinvar2[clinvar2$variant == "Y68H","clinvar_likely_pathog"] <- 0 ## The 2017 Pathogenic Assertion by GeneDx gives good supporting evidence of pathogenicity assertion
clinvar2[clinvar2$variant == "L108P","clinvar_likely_pathog"] <- 0 ## The 2014 Pathogenic Assertion by GeneDx gives good supporting evidence of pathogenicity assertion
clinvar2[clinvar2$variant == "G127R","clinvar_likely_pathog"] <- 0 ## The Assertion provided by GeneDx gives good supporting evidence of pathogenicity
clinvar2[clinvar2$variant == "R130L","clinvar_likely_pathog"] <- 0 ## The germline assertions for R130L is Pathogenic, whereas somatic assertions are likely pathogenic (and I'm only considering germline for downstream analyses)
clinvar2[clinvar2$variant == "R130Q","clinvar_likely_pathog"] <- 0 ## The germline assertions for R130Q is Pathogenic, whereas somatic assertions are likely pathogenic (and I'm only considering germline for downstream analyses)
clinvar2[clinvar2$variant == "G132V","clinvar_likely_pathog"] <- 0 ## The assertions made by GeneDx and OMIM for pathogenic are much better supported
clinvar2[clinvar2$variant == "R173C","clinvar_likely_pathog"] <- 0 ## The assertions for pathogenic made by the clinical lab and GeneDx are well supproted
clinvar2[clinvar2$variant == "R173H","clinvar_likely_pathog"] <- 0 ## The germline assertions for R173H are pathogenic, so no conflict at germline level.

#### This subsection finds duplicate annotations, and removes an uninformative one
clinvar2_duplicates <- subset(data.frame(table(clinvar2$variant)), Freq > 1)
duplicate_clinvar_rows <- c()
for(x in 1:nrow(clinvar2_duplicates)){
  duplicate_clinvar_rows <- append(duplicate_clinvar_rows,which(clinvar2_duplicates$Var1[x] == clinvar2$variant)[1])
}
clinvar2_single <- clinvar2[!(seq(1:nrow(clinvar2)) %in% duplicate_clinvar_rows),]
combined_clinvar <- merge(combined, clinvar2_single[,c("variant","clinvar_pathog","clinvar_likely_pathog","clinvar_uncertain","clinvar_likely_benign")], by = "variant", all.x = TRUE)

combined_clinvar[is.na(combined_clinvar$clinvar_pathog),"clinvar_pathog"] <- 0
combined_clinvar[is.na(combined_clinvar$clinvar_likely_pathog),"clinvar_likely_pathog"] <- 0
combined_clinvar[is.na(combined_clinvar$clinvar_uncertain),"clinvar_uncertain"] <- 0
combined_clinvar[is.na(combined_clinvar$clinvar_likely_benign),"clinvar_likely_benign"] <- 0
```

## Bringing in and setting up new GnomAD data

``` r
pten_gnomad <- read.csv(file = "input_datatables/PTEN_gnomAD_v3_ENSG00000171862_2019_11_11_13_05_32.csv", header = T, stringsAsFactors = F)
pten_gnomad <- subset(pten_gnomad, !(Annotation %in% c("splice_donor_variant","splice_donor")))

pten_gnomad$variant <- substr(pten_gnomad$Consequence,3,15)
pten_gnomad$position <- gsub("[A-Za-z]","",pten_gnomad$variant)
for(x in 1:nrow(pten_gnomad)){
  pten_gnomad$start[x] <- to_single_notation(substr(gsub("[0-9]","",pten_gnomad$variant[x]),1,3))
  pten_gnomad$end[x] <- to_single_notation(substr(gsub("[0-9]","",pten_gnomad$variant[x]),4,6))
  pten_gnomad$variant[x] <- paste(pten_gnomad$start[x],pten_gnomad$position[x],pten_gnomad$end[x],sep="")
}

colnames(pten_gnomad)[colnames(pten_gnomad) == "Allele.Count"] <- "gnomad_allele_count"
colnames(pten_gnomad)[colnames(pten_gnomad) == "Allele.Number"] <- "gnomad_allele_number"
pten_gnomad_variant <- pten_gnomad %>% group_by(variant) %>% summarize(gnomad_allele_count = sum(gnomad_allele_count), gnomad_allele_number = max(gnomad_allele_number))
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

``` r
combined_clinvar_gnomad <- merge(combined_clinvar, pten_gnomad_variant[,c("variant","gnomad_allele_count","gnomad_allele_number")], all.x = T)

combined_clinvar_gnomad$above_gnomad_allele_count_threshold_for_cowdens <- NA

collective_pten_cowdens_allele_frequency <- 1/400000

for(x in 1:nrow(combined_clinvar_gnomad)){
  if(!is.na(combined_clinvar_gnomad$gnomad_allele_count[x])){
    if(combined_clinvar_gnomad$gnomad_allele_count[x] > qbinom(0.99, size = combined_clinvar_gnomad$gnomad_allele_number[x], collective_pten_cowdens_allele_frequency / 0.95)){
      combined_clinvar_gnomad$above_gnomad_allele_count_threshold_for_cowdens[x] <- "above threshold"
    if(combined_clinvar_gnomad$gnomad_allele_count[x] <= qbinom(0.99, size = combined_clinvar_gnomad$gnomad_allele_number[x], collective_pten_cowdens_allele_frequency / 0.95)){
      combined_clinvar_gnomad$above_gnomad_allele_count_threshold_for_cowdens[x] <- "below threshold"
    }
    }
  }
}
```

## This is where the new biological analyses with the ClinVar and GnomAD data begins

``` r
custom_colorscale <- c("low" = "#3366ff","possibly_low" = "#b3d9ff","possibly_wt-like" = "#ffcccc","wt-like" = "#F8766D","dominant_negative" = "yellow","high" = "brown","unknown" = "grey75")

combined_for_plotting_clinvar <- rbind(
  combined_clinvar_gnomad %>% filter(snv == 1) %>% mutate(clinvar = "All SNV"),
  combined_clinvar_gnomad %>% filter(clinvar_pathog == 1) %>% mutate(clinvar = "Pathog"),
  combined_clinvar_gnomad %>% filter(clinvar_likely_pathog == 1) %>% mutate(clinvar = "Likely pathog"),
  combined_clinvar_gnomad %>% filter(clinvar_uncertain == 1) %>% mutate(clinvar = "Uncertain"),
  combined_clinvar_gnomad %>% filter(above_gnomad_allele_count_threshold_for_cowdens == "above threshold") %>% mutate(clinvar = "GnomAD inferred benign")
  )

all_snv_table <- data.frame(table((subset(combined_clinvar_gnomad, snv == 1))$abundance_class))
colnames(all_snv_table) <- c("abundance_class","count")
all_snv_table$count_interpreted <- all_snv_table$count
all_snv_table[all_snv_table$abundance_class == "unknown","count_interpreted"] <- 0
all_snv_table[all_snv_table$abundance_class == "low","count_interpreted"] / sum(all_snv_table$count_interpreted)
```

    ## [1] 0.2741722

``` r
pathogenic_table <- data.frame(table((subset(combined_clinvar_gnomad, clinvar_pathog == 1))$abundance_class))
colnames(pathogenic_table) <- c("abundance_class","count")
pathogenic_table$count_interpreted <- pathogenic_table$count
pathogenic_table[pathogenic_table$abundance_class == "unknown","count_interpreted"] <- 0
pathogenic_table[pathogenic_table$abundance_class == "low","count_interpreted"] / sum(pathogenic_table$count_interpreted)
```

    ## [1] 0.7878788

``` r
likelypathog_table <- data.frame(table((subset(combined_clinvar_gnomad, clinvar_likely_pathog == 1))$abundance_class))
colnames(likelypathog_table) <- c("abundance_class","count")
likelypathog_table$count_interpreted <- likelypathog_table$count
likelypathog_table[likelypathog_table$abundance_class == "unknown","count_interpreted"] <- 0
likelypathog_table[likelypathog_table$abundance_class == "low","count_interpreted"] / sum(likelypathog_table$count_interpreted)
```

    ## [1] 0.6190476

``` r
plp_table <- data.frame(table((subset(combined_clinvar_gnomad, clinvar_likely_pathog == 1 | clinvar_pathog == 1))$abundance_class))
colnames(plp_table) <- c("abundance_class","count")
plp_table$count_interpreted <- plp_table$count
plp_table[plp_table$abundance_class == "unknown","count_interpreted"] <- 0
plp_table[plp_table$abundance_class == "low","count_interpreted"] / sum(plp_table$count_interpreted)
```

    ## [1] 0.7196262

``` r
combined_for_plotting_clinvar$clinvar <- factor(combined_for_plotting_clinvar$clinvar, levels = c("All SNV","Pathog","Likely pathog","Uncertain","GnomAD inferred benign"))

Clinvar_plots_supplementary <- ggplot() + 
  theme_bw() + theme(legend.position = "top") +
  scale_fill_manual(values = custom_colorscale) + scale_color_manual(values = custom_colorscale) +
  geom_histogram(data = subset(combined_for_plotting_clinvar, class == "missense"), aes(x = score_abundance, fill = abundance_class), binwidth = 0.1, alpha = 0.5, position="stack", color = "black") + 
  facet_grid(rows = vars(clinvar), scale = "free_y")
Clinvar_plots_supplementary
```

    ## Warning: Removed 1078 rows containing non-finite values (stat_bin).

![](PTEN_composite_analysis_files/figure-gfm/Abundance%20score%20histogram-1.png)<!-- -->

``` r
ggsave(file = "plots/Clinvar_plots_supplementary.pdf", Clinvar_plots_supplementary, height = 140, width = 80, units = "mm")
```

    ## Warning: Removed 1078 rows containing non-finite values (stat_bin).

#### Printing out commands that can be used in Pymol (crystal structure 2d5r)

``` r
paste("select substrate, resi 1352","show spheres, substrate","color magenta, substrate", sep = ";")
```

    ## [1] "select substrate, resi 1352;show spheres, substrate;color magenta, substrate"

``` r
paste("select pathog_stable, not name c+n+o and resi", gsub(", ","+",toString(as.character(subset(combined_clinvar, class == "missense" & clinvar_pathog == 1 & snv == 1 & abundance_class == "wt-like")$position))),"; show spheres, pathog_stable; color red, pathog_stable")
```

    ## [1] "select pathog_stable, not name c+n+o and resi 19+24+93+12+130+130+14+15+217 ; show spheres, pathog_stable; color red, pathog_stable"

``` r
paste("select likely_pathog_stable, not name c+n+o and resi", gsub(", ","+",toString(as.character(subset(combined_clinvar, class == "missense" & clinvar_likely_pathog == 1 & snv == 1 & abundance_class == "wt-like")$position))),"; show spheres, likely_pathog_stable; color salmon, likely_pathog_stable")
```

    ## [1] "select likely_pathog_stable, not name c+n+o and resi 124+24+92+35+159+159 ; show spheres, likely_pathog_stable; color salmon, likely_pathog_stable"

``` r
## Rotate the pymol view
paste("rotate x, -90")
```

    ## [1] "rotate x, -90"

## Look for PTEN abundance variants in Blast data

``` r
blast <- read.delim(file = "input_datatables/PTEN_xml_blast_parsed_output.tsv", sep = "\t", header = TRUE, stringsAsFactors = FALSE)
blast_short <- subset(blast, align_length < 420)
blast_unique <- subset(blast_short, !(sciname %in% c("synthetic construct")))
blast_unique <- rbind(blast_unique[grep("XP", blast_unique$accession),],blast_unique[grep("NP", blast_unique$accession),])
blast_unique <- subset(blast_unique, variant_list != "['-85G', '-86Y', '-87L', '-88F', '-89T', '-90T']")
blast_unique_14 <- subset(blast_unique, variant_number <= 9)

pten_summary <- data.frame("organism" = c(), "variant" = c(), "score_abundance" = c(), "abundance_class" = c())

for(x in 1:nrow(blast_unique_14)){
  temp_list <- blast_unique_14$variant_list[x]
  temp_list2 <- unlist(strsplit(gsub("[^A-Z,0-9]","",temp_list),","))
  temp_organism <-gsub(" ","_",blast_unique_14$sciname[x])
  if(length(temp_list2)==0){pten_summary <- rbind(pten_summary, data.frame("organism" = temp_organism, "variant" = "WT", "score_abundance" = 1, "abundance_class" = "wt-like"))} else{
    for(y in 1:length(temp_list2 == 0)){
      temp_variant <- temp_list2[y]
      temp_value <- combined_clinvar[combined_clinvar$variant == temp_variant, "score_abundance"]
      temp_abund_class <- combined_clinvar[combined_clinvar$variant == temp_variant, "abundance_class"]
      if(length(temp_value)==0){temp_value <- NA}
      if(length(temp_abund_class)==0){temp_abund_class <- NA}
      pten_summary <- rbind(pten_summary, data.frame("organism" = temp_organism, "variant" = temp_variant, "score_abundance" = temp_value,"abundance_class" = temp_abund_class))
    }
  }
}
pten_summary <- subset(pten_summary, organism != "Neophocaena_asiaeorientalis_asiaeorientalis")

pten_tree <- read.newick(file = "input_datatables/PTEN_species_names.nwk")  #You need phytools for this
pten_tree_plot <- ggtree(pten_tree) + geom_tiplab(angle = 90) + coord_flip()
```

    ## Warning: `tbl_df()` is deprecated as of dplyr 1.0.0.
    ## Please use `tibble::as_tibble()` instead.
    ## This warning is displayed once every 8 hours.
    ## Call `lifecycle::last_warnings()` to see where this warning was generated.

``` r
pten_tree_plot
```

![](PTEN_composite_analysis_files/figure-gfm/Blast%20for%20PTEN%20data%20and%20abundance-1.png)<!-- -->

``` r
ggsave(file = "plots/pten_tree_plot.pdf", pten_tree_plot, height = 60*1.5, width = 178*1.5, units = "mm")

d = fortify(pten_tree)
d = subset(d, isTip)
label_order <- with(d, label[order(y, decreasing=F)])

pten_synonymous_5th <- quantile(subset(combined_clinvar, class == "synonymous")$score_abundance, 0.05, na.rm = T)
custom_colorscale <- c("low" = "#3366ff","possibly_low" = "#b3d9ff","possibly_wt-like" = "#ffcccc","wt-like" = "#F8766D","unknown" = "grey75")

pten_summary$organism <- as.character(pten_summary$organism)
for(x in 1:nrow(pten_summary)){
  pten_summary$organism[x] <- paste(unlist(strsplit(pten_summary$organism[x], split = "_"))[1],unlist(strsplit(pten_summary$organism[x], split = "_"))[2],sep = "_")
}

pten_summary[pten_summary$organism == "Neomonachus_schauinslandi","organism"] <- "Monachus_monachus"
label_order[!(label_order %in% pten_summary$organism)]
```

    ## character(0)

``` r
pten_summary$organism[!(pten_summary$organism %in% label_order)]
```

    ## character(0)

``` r
pten_summary$organism <- factor(pten_summary$organism, levels = c(label_order))

scientific_names <- read.csv(file = "input_datatables/Scientific_names.csv", header = TRUE, stringsAsFactors = FALSE)
scientific_names$organism <- gsub(" ", "_", scientific_names$sciname)

pten_summary2 <- merge(pten_summary, scientific_names[,c("organism","common")], by = "organism", all.x = TRUE)
pten_summary2 <- pten_summary2[order(pten_summary2$organism),]

common_order <- c()
for(x in 1:nrow(pten_summary2)){
  if(!is.na(pten_summary2$common[x]) & !(pten_summary2$common[x] %in% common_order)){
    common_order <- c(common_order, pten_summary2$common[x])
  }
}

pten_summary2$common <- factor(pten_summary2$common, levels = common_order)

variant_number <- data.frame(table(pten_summary2$common))
variant_number <- data.frame("common" = variant_number[,"Var1"])

pten_summary3 <- data.frame(unique((pten_summary2 %>% filter(variant != "WT"))[,c("variant","common","score_abundance","abundance_class")]))

variant_number2 <- data.frame(table(pten_summary3$common))
colnames(variant_number2) <- c("common","variant_number")

variant_number3 <- merge(variant_number, variant_number2, by = "common", all.x = TRUE)
variant_number3$common <- factor(variant_number3$common, levels = c(common_order))

pten_summary4 <- data.frame(unique(pten_summary3[,c("variant","score_abundance","abundance_class")]))

pten_abundance_organisms <- ggplot() + 
  theme_bw() + theme(axis.text.x = element_text(angle = -90, hjust = 0, vjust = 0.5), legend.position = "none", ) +
  scale_y_continuous(limits = c(0, 1.2)) + xlab(NULL) + ylab("Abundance score") +
  scale_color_manual(values = custom_colorscale) +
  geom_point(data = pten_summary2, aes(x = common, y = score_abundance, color = abundance_class)) +
  geom_text(data = variant_number3, aes(x = common, y = 0, label = variant_number), size = 3, color = "orange", angle = -90, hjust = 1)
pten_abundance_organisms
```

    ## Warning: Removed 49 rows containing missing values (geom_point).

![](PTEN_composite_analysis_files/figure-gfm/Blast%20for%20PTEN%20data%20and%20abundance-2.png)<!-- -->

``` r
ggsave(file = "plots/pten_abundance_organisms.pdf", pten_abundance_organisms, height = 60*1.5, width = 178*1.5, units = "mm")
```

    ## Warning: Removed 49 rows containing missing values (geom_point).

``` r
paste("We identified",nrow(pten_summary4),"missense changes from the human reference sequence.")
```

    ## [1] "We identified 46 missense changes from the human reference sequence."

``` r
paste("Of these, we had scores for",nrow(subset(pten_summary4, !is.na(score_abundance))),"variants.")
```

    ## [1] "Of these, we had scores for 21 variants."

``` r
paste(round(nrow(subset(pten_summary4, !is.na(score_abundance) & abundance_class == "low"))),"of these variants were low abundance")
```

    ## [1] "2 of these variants were low abundance"

``` r
homolog_variant_number_histogram <- ggplot() + 
  theme_bw() +
  theme(axis.text.x = element_text(angle = -90, hjust = 0, vjust = 0.5), legend.position = "none", panel.grid.major.x = element_blank(), panel.grid.minor.x = element_blank()) +
  xlab(NULL) + ylab("Amino acid differences from Humans") +
  scale_x_continuous(breaks = seq(0,10,1)) +
  geom_hline(yintercept = 0) +
  geom_histogram(data = variant_number3, aes(x = variant_number), binwidth = 1, fill = "grey50", color = "black", alpha = 0.5)
homolog_variant_number_histogram
```

![](PTEN_composite_analysis_files/figure-gfm/Blast%20for%20PTEN%20data%20and%20abundance-3.png)<!-- -->

``` r
ggsave(file = "plots/homolog_variant_number_histogram.pdf", homolog_variant_number_histogram, height = 40, width = 80, units = "mm")

paste("The median number of differences in related organisms was:",median(variant_number3$variant_number))
```

    ## [1] "The median number of differences in related organisms was: 1"

#### Make a single plot for PTEN All SNV, ClinVar, and Homolog

``` r
combined_clinvar_homolog <- rbind(
  (combined_clinvar_gnomad %>% filter(class == "missense") %>% mutate(grouping = "All\nmissense"))[,c("variant","grouping","score_abundance","abundance_class")],
  (combined_clinvar_gnomad %>% filter(clinvar_pathog == 1 | clinvar_likely_pathog == 1) %>% 
     mutate(grouping = "P/LP"))[,c("variant","grouping","score_abundance","abundance_class")],
  (pten_summary4 %>% mutate(grouping = "Homologs"))[,c("variant","grouping","score_abundance","abundance_class")],
    (combined_clinvar_gnomad %>% filter(above_gnomad_allele_count_threshold_for_cowdens == "above threshold") %>% mutate(grouping = "GnomAD\ninferred\nbenign"))[,c("variant","grouping","score_abundance","abundance_class")],
  (combined_clinvar_gnomad %>% filter(clinvar_uncertain == 1) %>% mutate(grouping = "Uncertain"))[,c("variant","grouping","score_abundance","abundance_class")]
)

combined_clinvar_homolog$grouping <- factor(combined_clinvar_homolog$grouping, levels = c("All\nmissense","P/LP","GnomAD\ninferred\nbenign","Homologs","Uncertain"))

custom_colorscale <- c("low" = "#3366ff","possibly_low" = "#b3d9ff","possibly_wt-like" = "#ffcccc","wt-like" = "#F8766D","unknown" = "grey75")

Clinvar_homolog_histograms <- ggplot() + 
  theme_bw() + theme(legend.position = "top", panel.grid.minor.y = element_blank()) +
  geom_vline(xintercept = synonymous_lowest_5percent, linetype = 2, alpha = 0.5) + 
  scale_fill_manual(values = custom_colorscale) + 
  scale_color_manual(values = custom_colorscale) +
  geom_histogram(data = combined_clinvar_homolog, aes(x = score_abundance, fill = abundance_class), binwidth = 0.1, alpha = 0.5, position="stack", color = "black") + 
  facet_grid(rows = vars(grouping), scale = "free_y")
Clinvar_homolog_histograms
```

    ## Warning: Removed 3452 rows containing non-finite values (stat_bin).

![](PTEN_composite_analysis_files/figure-gfm/Single%20plot%20for%20SNV,%20ClinVar,%20and%20Homologs-1.png)<!-- -->

``` r
ggsave(file = "plots/Clinvar_homolog_histograms.pdf", Clinvar_homolog_histograms, height = 125, width = 90, units = "mm")
```

    ## Warning: Removed 3452 rows containing non-finite values (stat_bin).

``` r
plp_summary <- data.frame(table((combined_clinvar_homolog %>% filter(grouping == "P/LP"))$abundance_class))
colnames(plp_summary) <- c("abundance_class","count")

paste("Of the",sum(plp_summary$count),"pathogenic or likely pathogenic variants of PTEN in ClinVar, we were able to give abundance interpretations for",sum(subset(plp_summary, abundance_class != "unknown")$count),"variants.")
```

    ## [1] "Of the 181 pathogenic or likely pathogenic variants of PTEN in ClinVar, we were able to give abundance interpretations for 107 variants."

``` r
plp_summary$interpreted_count <- plp_summary$count
plp_summary[plp_summary$abundance_class == "unknown","interpreted_count"] <- 0

plp_summary$interpreted_freq <- round(plp_summary$interpreted_count / sum(plp_summary$interpreted_count),2)
plp_summary
```

    ##    abundance_class count interpreted_count interpreted_freq
    ## 1              low    77                77             0.72
    ## 2     possibly_low     9                 9             0.08
    ## 3 possibly_wt-like     6                 6             0.06
    ## 4          unknown    74                 0             0.00
    ## 5          wt-like    15                15             0.14

#### Look at clustering of well-represented positions

``` r
orig_positional_coverage <- combined %>% filter(!is.na(score_orig) & class == "missense") %>% count(position) %>% count(n)
```

    ## Storing counts in `nn`, as `n` already present in input
    ## ℹ Use `name = "new_name"` to pick a new name.

``` r
composite_positional_coverage <- combined %>% filter(!is.na(score_abundance) & class == "missense") %>% count(position) %>% count(n)
```

    ## Storing counts in `nn`, as `n` already present in input
    ## ℹ Use `name = "new_name"` to pick a new name.

``` r
positional_coverage_frame <- merge(orig_positional_coverage,composite_positional_coverage, by = "n"); colnames(positional_coverage_frame) <- c("coverage","orig","composite")
positional_coverage_frame_melted <- melt(positional_coverage_frame, "coverage")

ggplot() + scale_x_continuous(limits = c(0.5,19.5), expand = c(0,1), breaks = seq(1,19,2)) +
  geom_bar(data = positional_coverage_frame_melted, aes(x = coverage, y = value, fill = variable), stat = "identity", position = "dodge", color = "black")
```

![](PTEN_composite_analysis_files/figure-gfm/Looking%20at%20well-characterized%20positions-1.png)<!-- -->

``` r
pten_missense <- subset(combined, class == "missense" & variant != "wt" & variant != "WT")

pten_seq <- "MTAIIKEIVSRNKRRYQEDGFDLDLTYIYPNIIAMGFPAERLEGVYRNNIDDVVRFLDSKHKNHYKIYNLCAERHYDTAKFNCRVAQYPFEDHNPPQLELIKPFCEDLDQWLSEDDNHVAAIHCKAGKGRTGVMICAYLLHRGKFLKAQEALDFYGEVRTRDKKGVTIPSQRRYVYYYSYLLKNHLDYRPVALLFHKMMFETIPMFSGGTCNPQFVVCQLKVKIYSSNSGPTRREDKFMYFEFPQPLPVCGDIKVEFFHKQNKMLKKDKMFHFWVNTFFIPGPEETSEKVENGSLCDQEIDSICSIERADNDKEYLVLTLTKNDLDKANKDKANRYFSPNFKVKLYFTKTVEEPSNPEASSSTSVTPDVSDNEPDHYRYSDTTDSDPENEPFDEDQHTQITKV"

pten_aa_num <- nchar(pten_seq)
pten_df <- data.frame("position" = seq(1,pten_aa_num,1),
                      "A"= rep(NA,pten_aa_num), "C"= rep(NA,pten_aa_num), "D"= rep(NA,pten_aa_num), "E"= rep(NA,pten_aa_num), "F"= rep(NA,pten_aa_num), "G"= rep(NA,pten_aa_num),
                      "H"= rep(NA,pten_aa_num), "I"= rep(NA,pten_aa_num), "K"= rep(NA,pten_aa_num), "L"= rep(NA,pten_aa_num), "M"= rep(NA,pten_aa_num), "N"= rep(NA,pten_aa_num),
                      "P"= rep(NA,pten_aa_num), "Q"= rep(NA,pten_aa_num), "R"= rep(NA,pten_aa_num), "S"= rep(NA,pten_aa_num), "T"= rep(NA,pten_aa_num), "V"= rep(NA,pten_aa_num),
                      "W"= rep(NA,pten_aa_num), "Y"= rep(NA,pten_aa_num))

for(y in 1:nchar(pten_seq)){pten_df[y,substr(pten_seq,y,y)] <- 1}
for(x in 1:nrow(pten_missense)){
  pten_df[pten_missense$position[x],pten_missense$end[x]] <- pten_missense$score_abundance[x]}

pten_df <- subset(pten_df, !is.na(position))

abundance_normal_percentile_low <- median((subset(combined_clinvar_gnomad, class == "synonymous"))$score_total, na.rm = T)
abundance_normal_percentile_high <- quantile((subset(combined_clinvar_gnomad, class == "synonymous"))$score_total, 0.95, na.rm = T) 

abundance_low_percentile <- median((subset(combined_clinvar_gnomad, class == "nonsense"))$score_total, na.rm = T) #quantile(normal_dist_fit_low$prob, 0.90)

pten_double3 <- pten_df[2:nrow(pten_df),]

pten_double3$fraction_below_wt <- 0
for(x in 1:nrow(pten_double3)){
  pten_double3$fraction_below_wt[x] <- sum(na.omit(unlist(pten_double3[x,2:ncol(pten_double3)])) < abundance_normal_percentile_low) / length(na.omit(unlist(pten_double3[x,2:ncol(pten_double3)])))
}

pten_lower_threshold <- as.numeric(abundance_low_percentile)
pten_upper_threshold <- as.numeric(abundance_normal_percentile_high)


## Double hclust
pten_double <- pten_df[,2:21]
rownames(pten_double) <- pten_df[,1]


## Subsetting only for positions with 18 or more variants
pten_double$count <- NA
for(x in 1:nrow(pten_double)){
  pten_double$count[x] <- sum(!is.na(pten_double[x,]))
}

pten_double <- subset(pten_double, count >= 18)
pten_double <- pten_double[,1:20]
pten_double2 <- pten_double

for(x in 1:nrow(pten_double2)){
  for(y in 1:ncol(pten_double2)){
    if(is.na(pten_double2[x,y]) == TRUE){
      pten_double2[x,y] <- mean(unlist(pten_double2[x,]), na.rm = TRUE)
    }
  }
}

row.order <- hclust(dist(pten_double2))$order
col.order <- hclust(dist(t(pten_double2)))$order

pten_double_label_order <- rev(rownames(pten_double2[row.order, col.order]))
pten_double_variable_order <- colnames(pten_double2[row.order, col.order])
pten_double_variable_order <- c("G","S","T","C","A","M","W","Y","F","L","I","V","D","E","N","Q","H","K","R","P")

pten_double$label <- rownames(pten_double)
pten_double2_melt <- melt(pten_double, id = "label")

for(x in 1:nrow(pten_double2_melt)){
  pten_double2_melt$value[x] <- as.numeric(as.character(pten_double2_melt$value[x]))
  if(pten_double2_melt$value[x] <= pten_lower_threshold & !(is.na(pten_double2_melt$value[x]))){pten_double2_melt$value[x] <- pten_lower_threshold}
  if(pten_double2_melt$value[x] >= pten_upper_threshold & !(is.na(pten_double2_melt$value[x]))){pten_double2_melt$value[x] <- pten_upper_threshold}
}

pten_double2_melt <- subset(pten_double2_melt, label != 1)
pten_double2_melt$label <- factor(pten_double2_melt$label, levels = pten_double_label_order)
pten_double2_melt$variable <- factor(pten_double2_melt$variable, levels = pten_double_variable_order)

pten_mutational_spectra <- ggplot() + 
  xlab(NULL) + ylab(NULL) + theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1)) +
  scale_fill_gradientn(colours = c("blue","white","red"), values = rescale(c(pten_lower_threshold,1,1.5)), limits=c(pten_lower_threshold,1.5)) +
  geom_tile(data = pten_double2_melt, aes(x = label, y = variable, fill = value))
pten_mutational_spectra
```

![](PTEN_composite_analysis_files/figure-gfm/Looking%20at%20well-characterized%20positions-2.png)<!-- -->

``` r
ggsave(file = "plots/pten_abundance_mutational_spectra.pdf", pten_mutational_spectra, height = 80, width = 178*2, units = "mm")

write.csv(file = "output_datatables/pten_abundance_imputed.csv", pten_double2, quote = FALSE, row.names = FALSE)
```

#### Calculate gini coefficient to separate most mutation intolerant positions

``` r
gini_frame <- data.frame("position" = as.character(rownames(pten_double2)))
gini_frame$gini <- 0
for(x in 1:nrow(gini_frame)){gini_frame$gini[x] <- gini(unlist(pten_double2[x,]))}

paste("Minimum Gini coefficient:", round(min(gini_frame$gini, na.rm = T),2))
```

    ## [1] "Minimum Gini coefficient: 0.03"

``` r
paste("Maximum Gini coefficient:", round(max(gini_frame$gini, na.rm = T),2))
```

    ## [1] "Maximum Gini coefficient: 0.35"

``` r
Gini_coefficient_plot <- ggplot() +
  theme_bw() + 
  scale_y_continuous(expand = c(0,0.1)) +
  geom_hline(yintercept = 0, size = 1.5) +
  geom_histogram(data = subset(gini_frame, gini <= 0.121), aes(x = gini), binwidth = 0.02, color = "black", fill = "blue", alpha = 0.8) +
  geom_histogram(data = subset(gini_frame, gini > 0.121 & gini <= 0.24), aes(x = gini), binwidth = 0.02, color = "black", fill = "thistle2", alpha =  0.8) +
  geom_histogram(data = subset(gini_frame, gini > 0.24), aes(x = gini), binwidth = 0.02, color = "black", fill = "red", alpha =  0.8)
Gini_coefficient_plot
```

![](PTEN_composite_analysis_files/figure-gfm/Gini%20coefficient-1.png)<!-- -->

``` r
ggsave(file = "plots/Gini_coefficient_plot.pdf", Gini_coefficient_plot, height = 35, width = 35, units = "mm")

paste("select mut_intolerant_abundance, resi",gsub(", ","+",toString(as.numeric(as.character((mutation_intolerant_positions <- gini_frame %>% filter(gini > 0.25))$position)))))
```

    ## [1] "select mut_intolerant_abundance, resi 67+173+181+243+249+251+253+325+326+343"

``` r
paste("select polar_mut_intolerant_abundance, resi 251+173+326+169")
```

    ## [1] "select polar_mut_intolerant_abundance, resi 251+173+326+169"

#### Combine Gini coefficient with clustered heatmap

``` r
gini_frame2 <- gini_frame
colnames(gini_frame2) <- c("label","value")

gini_frame2[gini_frame2$value <= 0.07191892, "value"] <- 0.072
gini_frame2[gini_frame2$value >= 0.07191892 & gini_frame2$value <= 0.121, "value"] <- 0.072
gini_frame2[gini_frame2$value > 0.24, "value"] <- 1.5
gini_frame2[gini_frame2$value > 0.121 & gini_frame2$value <= 0.24, "value"] <- 0.9

gini_frame2$variable <- "Gini"
pten_double2_melt_gini <- rbind(pten_double2_melt, gini_frame2)

## Frame for denoting WT resudiues
pten_residues <- data.frame("position" = seq(1,nchar(pten_seq)), "residue" = NA)
for(x in 1:nrow(pten_residues)){pten_residues$residue[x] <- substr(pten_seq,x,x)}
pten_residues2 <- subset(pten_residues, position %in% gini_frame2$label)
pten_residues2$position <- as.character(pten_residues2$position)
pten_residues2$position <- factor(pten_residues2$position, levels = pten_double_label_order)
pten_residues2$residue <- factor(pten_residues2$residue, levels = pten_double_variable_order)

pten_mutational_spectra <- ggplot() +
  xlab(NULL) + ylab(NULL) + 
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1)) +
  scale_fill_gradientn(colours = c("blue","white","red"), values = rescale(c(pten_lower_threshold,1,1.5)), limits=c(pten_lower_threshold-0.1,1.5)) +
  geom_tile(data = pten_double2_melt_gini, aes(x = label, y = variable, fill = value)) +
  geom_point(data = pten_residues2, aes(x = position, y = residue)) + 
  geom_hline(yintercept = 20.5)
pten_mutational_spectra
```

![](PTEN_composite_analysis_files/figure-gfm/Combined%20gini%20and%20mutational%20spectra-1.png)<!-- -->

``` r
ggsave(file = "plots/pten_abundance_mutational_spectra.pdf", pten_mutational_spectra, height = 65, width = 175*1.2, units = "mm")
```

## Comparisons of PTEN abundance and activity

#### Now let’s add in PTEN functional data

``` r
# Import the supplementary data from the Mighell et al AJHG paper
pten_func <- read.delim(file = "input_datatables/Mighell_PTEN_phosphatase_data.csv", sep = ",", header = TRUE, stringsAsFactors = FALSE)
pten_func <- pten_func[,c("Variant..one.letter.","Cum_score","Cum_SE","High_conf")]
colnames(pten_func) <- c("variant","func","func_se","high_conf")
pten_func$position <- gsub("[^0-9]","",pten_func$variant)
pten_func$variant <- gsub("\\*","X",pten_func$variant)
for(x in 1:nrow(pten_func)){
  pten_func$start[x] <- substr(gsub("[^A-Z]","",pten_func$variant[x]),1,1)
  pten_func$end[x] <- substr(gsub("[^A-Z]","",pten_func$variant[x]),2,2)
}
pten_func <- subset(pten_func, end != "" & position != 1)
pten_func$func4 <- -(pten_func$func / quantile((pten_func$func), 0.05, na.rm = TRUE)) + 1
pten_func$func5 <- ((pten_func$func4) - quantile((pten_func$func4), 0.05, na.rm = TRUE)) / (1 - quantile((pten_func$func4), 0.05, na.rm = TRUE))
pten_func$score_activity <- pten_func$func5

combined_abund_act <- merge(combined_clinvar, pten_func[,c("variant","score_activity","high_conf")], by = "variant", all.x = T)[c("variant","position","snv","class","score_abundance","abundance_class","score_activity","high_conf","clinvar_pathog","clinvar_likely_pathog","clinvar_uncertain")]

## Set some boundaries
abundance_syn_5th <- quantile(subset(combined_abund_act, class == "synonymous")$score_abundance,0.05,na.rm = T)
abundance_nonsense_5th <- quantile(subset(combined_abund_act, position > 50 & position < 350 & class == "nonsense")$score_abundance,0.95, na.rm = T)

pten_func_syn <- -1.11
pten_func_syn3 <- -(pten_func_syn / quantile((pten_func$func), 0.05, na.rm = TRUE)) + 1
pten_func_syn4 <- ((pten_func_syn3) - quantile((pten_func$func4), 0.05, na.rm = TRUE)) / (1 - quantile((pten_func$func4), 0.05, na.rm = TRUE))
activity_syn_5th <- pten_func_syn4

pten_func_nonsense <- -2.13
pten_func_nonsense3 <- -(pten_func_nonsense / quantile((pten_func$func), 0.05, na.rm = TRUE)) + 1
pten_func_nonsense4 <- ((pten_func_nonsense3) - quantile((pten_func$func4), 0.05, na.rm = TRUE)) / (1 - quantile((pten_func$func4), 0.05, na.rm = TRUE))
activity_nonsense_5th <- pten_func_nonsense4

count_abundance_scores <- nrow(subset(combined_abund_act, !is.na(score_abundance) & class == "missense"))
paste("Number of variants with abundance scores:", count_abundance_scores)
```

    ## [1] "Number of variants with abundance scores: 4387"

``` r
count_activity_scores <- nrow(subset(combined_abund_act, !is.na(score_activity) & class == "missense" & high_conf == T))
paste("Number of variants with activity scores:", count_activity_scores)
```

    ## [1] "Number of variants with activity scores: 6561"

#### Making a comparison of abundance and functional data

``` r
complete_abund_act <- subset(combined_abund_act, !is.na(score_abundance) & !(is.na(score_activity)))
complete_abund_act$abund_act_class <- "NA"

for(x in 1:nrow(complete_abund_act)){
  if(!(is.na(complete_abund_act$score_activity[x])) & !(is.na(complete_abund_act$score_abundance[x]))){
    if((complete_abund_act$abundance_class[x] == "low") & (complete_abund_act$score_activity[x] > activity_syn_5th)){complete_abund_act$abund_act_class[x] <- "2_unstable_active"}
    if((complete_abund_act$abundance_class[x] == "wt-like") & (complete_abund_act$score_activity[x] < activity_nonsense_5th)){complete_abund_act$abund_act_class[x] <- "4_stable_inactive"}
    if((complete_abund_act$abundance_class[x] == "low") & (complete_abund_act$score_activity[x] < activity_nonsense_5th)){complete_abund_act$abund_act_class[x] <- "3_unstable_inactive"}
    if((complete_abund_act$abundance_class[x] == "wt-like") & (complete_abund_act$score_activity[x] > activity_syn_5th)){complete_abund_act$abund_act_class[x] <- "1_stable_active"}
  }
}

complete_abund_act$abund_act_class <- factor(complete_abund_act$abund_act_class, levels = c("2_unstable_active","4_stable_inactive","3_unstable_inactive","1_stable_active","NA"))

custom_colorscale2 <- c("2_unstable_active" = "turquoise","4_stable_inactive" = "orange","3_unstable_inactive" = "purple","1_stable_active" = "dark green", "NA" = "grey75")
complete_abund_act_missense <- subset(complete_abund_act, class == "missense" & !is.na(score_abundance) & !(is.na(score_activity)))
```

``` r
complete_table <- data.frame(table(complete_abund_act_missense$position))
complete_table <- complete_table[order(complete_table$Freq, decreasing = T),]

loss_of_abundance_table <- data.frame(table(subset(complete_abund_act_missense, abund_act_class == "2_unstable_active")$position))
loss_of_abundance_table <- loss_of_abundance_table[order(loss_of_abundance_table$Freq, decreasing = T),]

loss_of_activity_table <- data.frame(table(subset(complete_abund_act_missense, abund_act_class == "4_stable_inactive")$position))
loss_of_activity_table <- loss_of_activity_table[order(loss_of_activity_table$Freq, decreasing = T),]

complete_table <- merge(complete_table, loss_of_abundance_table, by = "Var1", all.x = T)
complete_table <- merge(complete_table, loss_of_activity_table, by = "Var1", all.x = T)
colnames(complete_table) <- c("position","complete","loss_of_abundance","loss_of_activity")
complete_table[is.na(complete_table)] <- 0

loss_of_both_table <- data.frame(table(subset(complete_abund_act_missense, abund_act_class == "3_unstable_inactive")$position))
loss_of_both_table <- loss_of_both_table[order(loss_of_both_table$Freq, decreasing = T),]
colnames(loss_of_both_table) <- c("position","loss_of_both")

complete_table <- merge(complete_table, loss_of_both_table, by = "position", all.x = T)
complete_table[is.na(complete_table)] <- 0

complete_table$percent_loss_of_abundance <- complete_table$loss_of_abundance / complete_table$complete * 100
complete_table$percent_loss_of_activity <- complete_table$loss_of_activity / complete_table$complete * 100
complete_table$percent_loss_of_both <- complete_table$loss_of_both / complete_table$complete * 100

low_abund_act_diff <- subset(complete_table, percent_loss_of_abundance >= 50 & complete >= 5)
high_abund_act_diff <- subset(complete_table, percent_loss_of_activity >= 50 & complete >= 5)
low_total <- subset(complete_table, percent_loss_of_both >= 50 & complete >= 5)

paste("select low_diff, resi",gsub(", ","+",toString(low_abund_act_diff$position)), "and not name c+n+o")
```

    ## [1] "select low_diff, resi 58+66+169+172+188+246+247+258+270+274+278+280+322+331+337+348+388 and not name c+n+o"

``` r
paste("select high_diff, resi",gsub(", ","+",toString(high_abund_act_diff$position)), "and not name c+n+o")
```

    ## [1] "select high_diff, resi 15+47+92+123+125+130+159+333+401 and not name c+n+o"

``` r
paste("select low, resi",gsub(", ","+",toString(low_total$position)), "and not name c+n+o")
```

    ## [1] "select low, resi 25+27+28+35+53+56+57+61+67+68+95+101+104+105+107+108+111+119+120+122+131+136+137+140+148+166+170+175+177+195+217+241+249+252+253+255+271+275+277+325+326+346 and not name c+n+o"

``` r
quadrant_plot <- ggplot() + 
  theme_classic() +
  theme(legend.position = "none", panel.grid.major = element_line("grey95")) +
  xlab("Abundance score") + ylab("Activity score") +
  scale_x_continuous(breaks = c(0,1)) + 
  scale_y_continuous(breaks = c(0,1)) +
  scale_color_manual(values = custom_colorscale2) +
  geom_point(data = complete_abund_act_missense, aes(x = score_abundance, y = score_activity, color = abund_act_class), alpha = 0.2) +
  geom_hline(yintercept = activity_syn_5th, linetype = 2, color = "red", alpha = 0.5) +
  geom_hline(yintercept = activity_nonsense_5th, linetype = 2, color = "blue", alpha = 0.5) +
  geom_vline(xintercept = quantile(subset(complete_abund_act_missense, abundance_class == "wt-like")$score_abundance,0.01, na.rm = T), linetype = 2, color = "red", alpha = 0.5) +
  geom_vline(xintercept = quantile(subset(complete_abund_act_missense, abundance_class == "low")$score_abundance,0.99), linetype = 2, color = "blue", alpha = 0.5)
quadrant_plot
```

![](PTEN_composite_analysis_files/figure-gfm/How%20about%20literally%20just%20subtracting%20abundance%20by%20activity-1.png)<!-- -->

``` r
ggsave(file = "plots/quadrant_plot.pdf", quadrant_plot, height = 80, width = 80, units = "mm")

paste("Number of confidently assessed PTEN variants:",nrow(subset(complete_abund_act_missense, abund_act_class != "NA")))
```

    ## [1] "Number of confidently assessed PTEN variants: 2376"

``` r
sfari <- read.delim(file = "input_datatables/Sfari_20191111.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% filter(variant_type %in% c("missense_variant","stop_gained")) %>% filter(residue_change != "-")

sfari$variant3 <- substr(sfari$residue_change, 3, 18)
sfari$start <- "NA"
sfari$end <- "NA"
for(x in 1:nrow(sfari)){
  sfari$start[x] <- substr(sfari$variant3[x], 1, 3)
  sfari$end[x] <- substr(sfari$variant3[x], nchar(toString(sfari$variant3[x]))-2, nchar(toString(sfari$variant3[x])))}
sfari$position <- gsub("[^0-9]", "", sfari$variant3)
for (x in 1:nrow(sfari)){
  sfari$start[x] <- to_single_notation(sfari$start[x])
  sfari$end[x] <- to_single_notation(sfari$end[x])
}
sfari$variant <- paste(sfari$start, sfari$position, sfari$end, sep ="")

sfari_summary <- data.frame(table(sfari$variant))
colnames(sfari_summary) <- c("variant","sfari")

complete_abund_act_missense2 <- merge(complete_abund_act_missense, sfari_summary, by = "variant", all.x = T)
complete_abund_act_missense2[is.na(complete_abund_act_missense2$sfari),"sfari"] <- 0

clinvar_abundance_activity_aggregate <- rbind(
  (complete_abund_act_missense2 %>% filter(snv == 1) %>% mutate(grouping = "All_SNV"))[,c("variant","grouping","score_abundance","abund_act_class")],
  (complete_abund_act_missense2 %>% filter((clinvar_pathog == 1 | clinvar_likely_pathog == 1) & snv == 1) %>% mutate(grouping = "P_LP"))[,c("variant","grouping","score_abundance","abund_act_class")],
  (complete_abund_act_missense2 %>% filter(clinvar_uncertain == 1 & snv == 1) %>% mutate(grouping = "VUS"))[,c("variant","grouping","score_abundance","abund_act_class")],
  (complete_abund_act_missense2 %>% filter(snv == 1 & sfari >= 1) %>% mutate(grouping = "ASD"))[,c("variant","grouping","score_abundance","abund_act_class")])

clinvar_abundance_activity_aggregate$grouping <- factor(clinvar_abundance_activity_aggregate$grouping, levels = c("All_SNV","P_LP","VUS","ASD"))
clinvar_abundance_activity_aggregate2 <- subset(clinvar_abundance_activity_aggregate, abund_act_class != "NA")

clinvar_abundance_activity_aggregate2_summary <- data.frame(table(subset(clinvar_abundance_activity_aggregate2, grouping == "All_SNV")$abund_act_class))
clinvar_abundance_activity_aggregate2_summary <- merge(clinvar_abundance_activity_aggregate2_summary, data.frame(table(subset(clinvar_abundance_activity_aggregate2, grouping == "P_LP")$abund_act_class)), by = "Var1")
clinvar_abundance_activity_aggregate2_summary <- merge(clinvar_abundance_activity_aggregate2_summary, data.frame(table(subset(clinvar_abundance_activity_aggregate2, grouping == "VUS")$abund_act_class)), by = "Var1")
clinvar_abundance_activity_aggregate2_summary <- merge(clinvar_abundance_activity_aggregate2_summary, data.frame(table(subset(clinvar_abundance_activity_aggregate2, grouping == "ASD")$abund_act_class)), by = "Var1")
```

    ## Warning in merge.data.frame(clinvar_abundance_activity_aggregate2_summary, :
    ## column names 'Freq.x', 'Freq.y' are duplicated in the result

``` r
colnames(clinvar_abundance_activity_aggregate2_summary) <- c("abund_act_class","All_SNV","P_LP","VUS","ASD")

clinvar_abundance_activity_aggregate2_summary <- clinvar_abundance_activity_aggregate2_summary %>% filter(abund_act_class != "NA") %>%  mutate(freq_all_snv = All_SNV / sum(All_SNV), freq_P_LP = P_LP / sum(P_LP), freq_VUS = VUS / sum(VUS), freq_ASD = ASD / sum(ASD))

clinvar_abundance_activity_aggregate2_summary_melt <- melt(clinvar_abundance_activity_aggregate2_summary[,c("abund_act_class","freq_all_snv","freq_P_LP","freq_VUS","freq_ASD")], id = "abund_act_class")
clinvar_abundance_activity_aggregate2_summary_melt$abund_act_class <- factor(clinvar_abundance_activity_aggregate2_summary_melt$abund_act_class, levels = c("3_unstable_inactive","4_stable_inactive","2_unstable_active","1_stable_active"))

custom_colorscale3 <- c("3_unstable_inactive" = "purple","4_stable_inactive" = "orange","2_unstable_active" = "turquoise","1_stable_active" = "dark green")

clinvar_abundance_activity_aggregate2_summary_melt$variable <- as.character(clinvar_abundance_activity_aggregate2_summary_melt$variable)

clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_all_snv","variable"] <- "All SNV"
clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_P_LP","variable"] <- "P/LP"
clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_VUS","variable"] <- "VUS"
clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_ASD","variable"] <- "ASD"

clinvar_abundance_activity_aggregate2_summary_melt$variable <- factor(clinvar_abundance_activity_aggregate2_summary_melt$variable, levels = c("All SNV","P/LP","VUS","ASD"))

Clinvar_abundance_activity_barplots <- ggplot() + 
  theme(legend.position = "top", panel.grid.major.x = element_blank()) +
  xlab(NULL) + ylab("Fraction of variants") +
  scale_fill_manual(values = custom_colorscale3) +
  geom_bar(data = clinvar_abundance_activity_aggregate2_summary_melt, aes(x = variable, y = value, fill = abund_act_class), stat = "identity", alpha = 0.6, color = "black")
Clinvar_abundance_activity_barplots
```

![](PTEN_composite_analysis_files/figure-gfm/Look%20at%20PHTS%20variants%20in%20ClinVar%20and%20autism-associated%20variants%20in%20sfari-1.png)<!-- -->

``` r
ggsave(file = "plots/Clinvar_abundance_activity_barplots.pdf", Clinvar_abundance_activity_barplots, height = 60, width = 80, units = "mm")

#### Noting how many VUS are in one of the three loss-of-function categories
paste("The number of VUS in the dataset:",nrow(complete_abund_act_missense %>% filter(clinvar_uncertain != 0)))
```

    ## [1] "The number of VUS in the dataset: 192"

``` r
paste("The number of VUS in the dataset that are low activity or low abundance:",nrow(complete_abund_act_missense %>% filter(clinvar_uncertain != 0 & (abundance_class == "low" | score_activity < activity_nonsense_5th))))
```

    ## [1] "The number of VUS in the dataset that are low activity or low abundance: 58"

``` r
impact <- read.delim(file = "input_datatables/cancer_data/IMPACT_PTEN.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(variant = gsub("[*]","X",Protein.Change)) %>% group_by(Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant)) %>% mutate(length = nchar(variant)) %>% filter(length <= 5) %>% filter(!(Sample.ID %in% c("P-0000422-T02-IM3","P-0000657-T02-IM5","P-0001442-T02-IM5","P-0000997-T02-IM3","P-0002647-T02-IM5","P-0002738-T02-IM5","P-0002825-T02-IM5","P-0003101-T02-IM5","P-0003101-T03-","P-0006970-T02-IM5IM5","P-0003241-T02-IM5","P-0004910-T04-IM5","P-0004954-T02-IM5","P-0005361-T02-IM5","P-0007076-T03-IM5","P-0008380-T02-IM5")))
```

    ## `summarise()` regrouping output by 'Sample.ID' (override with `.groups` argument)

``` r
impact$type <- ""

impact[grepl("Uterine",impact$Cancer.Type),"type"] <- "uterine"
impact[grepl("Lung",impact$Cancer.Type),"type"] <- "lung"
impact[grepl("Glio",impact$Cancer.Type),"type"] <- "glioma"
impact[grepl("Astro",impact$Cancer.Type),"type"] <- "glioma"
impact[grepl("Breast",impact$Cancer.Type),"type"] <- "breast"
impact[grepl("Prostate",impact$Cancer.Type),"type"] <- "prostate"
impact[grepl("Colon",impact$Cancer.Type),"type"] <- "colorectal"
impact[grepl("Gastrointestinal",impact$Cancer.Type),"type"] <- "colorectal"
impact[grepl("Skin",impact$Cancer.Type),"type"] <- "skin"
impact[grepl("Melanoma",impact$Cancer.Type),"type"] <- "skin"
impact[grepl("Cutaneous",impact$Cancer.Type),"type"] <- "skin"
impact[grepl("Merkel",impact$Cancer.Type),"type"] <- "skin"
impact[grepl("Renal",impact$Cancer.Type),"type"] <- "renal"
impact[grepl("Rectal",impact$Cancer.Type),"type"] <- "colorectal"
impact[grepl("Anal",impact$Cancer.Type),"type"] <- "colorectal"
impact[grepl("Bladder",impact$Cancer.Type),"type"] <- "bladder"
impact[grepl("Esophageal",impact$Cancer.Type),"type"] <- "esophagus"
impact[grepl("Larynx",impact$Cancer.Type),"type"] <- "esophagus"
impact[grepl("Gastroesophageal",impact$Cancer.Type),"type"] <- "esophagus"
impact_na <- impact[is.na(impact$type),]
impact2 <- impact[!is.na(impact$type),]

colorectal <- read.delim(file = "input_datatables/cancer_data/Colorectal_PTEN.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(variant = gsub("[*]","X",Protein.Change)) %>% group_by(Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant)) %>% mutate(length = nchar(variant)) %>% filter(length <= 5) %>% mutate(type = "colorectal") %>% filter(!(Sample.ID %in% c("P-0000997-T02-IM3","TCGA-A6-6780-01")))
```

    ## `summarise()` regrouping output by 'Sample.ID' (override with `.groups` argument)

``` r
glioma <- read.delim(file = "input_datatables/cancer_data/Glioma_PTEN.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(Cancer.Type = "Glioma", variant = gsub("[*]","X",Protein.Change)) %>% group_by(Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant)) %>% mutate(length = nchar(variant)) %>% filter(length <= 5) %>% mutate(type = "glioma") %>% filter(!(Sample.ID %in% c("Patient-21-CSF-LP","Patient-21-CSF-VP","Patient-30-CSF-LP","Patient-30-CSF-VP","Patient-25-CSF")))
```

    ## `summarise()` regrouping output by 'Sample.ID' (override with `.groups` argument)

``` r
#glioma <- glioma[,c("Sample.ID","Cancer.Type","variant","length","type")]

prostate <- read.delim(file = "input_datatables/cancer_data/Prostate_PTEN.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(variant = gsub("[*]","X",Protein.Change)) %>% group_by(Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant)) %>% mutate(length = nchar(variant)) %>% filter(length <= 5) %>% mutate(type = "prostate") %>% filter(!(Sample.ID %in% c("P-0004910-T04-IM5","PM14-TM","PRAD-01115263-Tumor-SM-6WZF9","PRAD-6115393.0-Tumor-SM-7LGUF","SC_9062-Tumor","SC_9163_Tumor")))
```

    ## `summarise()` regrouping output by 'Sample.ID' (override with `.groups` argument)

``` r
esophagus <- read.delim(file = "input_datatables/cancer_data/Esophagus_PTEN.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(variant = gsub("[*]","X",Protein.Change)) %>% group_by(Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant)) %>% mutate(length = nchar(variant)) %>% filter(length <= 5) %>% mutate(type = "esophagus")
```

    ## `summarise()` regrouping output by 'Sample.ID' (override with `.groups` argument)

``` r
breast <- read.delim(file = "input_datatables/cancer_data/Breast_PTEN.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(variant = gsub("[*]","X",Protein.Change)) %>% group_by(Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant)) %>% mutate(length = nchar(variant)) %>% filter(length <= 5) %>% mutate(type = "breast") %>% filter(!(Sample.ID %in% c("MBC-MBCProject_6vTVHzur-Tumor-SM-GQCQV","MBC-MBCProject_GvHkH2Hk-Tumor-SM-AZ5HV","MBC-MBCProject_xBfJfri9-Tumor-SM-CGLAP","P-0000422-T02-IM3","P-0003241-T02-IM5","P-0004388-T02-IM5","SA429X5A-whole_genome","MTS-T0693")))
```

    ## `summarise()` regrouping output by 'Sample.ID' (override with `.groups` argument)

``` r
renal <- read.delim(file = "input_datatables/cancer_data/Renal_PTEN.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(variant = gsub("[*]","X",Protein.Change)) %>% group_by(Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant)) %>% mutate(length = nchar(variant)) %>% filter(length <= 5) %>% mutate(type = "renal")
```

    ## `summarise()` regrouping output by 'Sample.ID' (override with `.groups` argument)

``` r
skin <- read.delim(file = "input_datatables/cancer_data/Skin_PTEN.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(variant = gsub("[*]","X",Protein.Change)) %>% group_by(Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant)) %>% mutate(length = nchar(variant)) %>% filter(length <= 5) %>% mutate(type = "skin") %>% filter(!(Sample.ID %in% c("Pat_07_Post","Pat_11_Post","Pat_29_Post","Pat_58_Post","ME009")))
```

    ## `summarise()` regrouping output by 'Sample.ID' (override with `.groups` argument)

``` r
uterine <- read.delim(file = "input_datatables/cancer_data/Uterine_PTEN.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(variant = gsub("[*]","X",Protein.Change)) %>% group_by(Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant)) %>% mutate(length = nchar(variant)) %>% filter(length <= 5) %>% mutate(type = "uterine")
```

    ## `summarise()` regrouping output by 'Sample.ID' (override with `.groups` argument)

``` r
lung <- read.delim(file = "input_datatables/cancer_data/Lung_PTEN.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(variant = gsub("[*]","X",Protein.Change)) %>% group_by(Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant)) %>% mutate(length = nchar(variant)) %>% filter(length <= 5) %>% mutate(type = "lung") %>% filter(!(Sample.ID %in% c("LUAD-B01102-Tumor","LUAD-RT-S01702-Tumor","LUAD-RT-S01856-Tumor","P-0001442-T02-IM5","JHU-LX33-R")))
```

    ## `summarise()` regrouping output by 'Sample.ID' (override with `.groups` argument)

``` r
bladder <- read.delim(file = "input_datatables/cancer_data/Bladder_PTEN.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(variant = gsub("[*]","X",Protein.Change)) %>% group_by(Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant)) %>% mutate(length = nchar(variant)) %>% filter(length <= 5) %>% mutate(type = "bladder") %>% filter(!(Sample.ID %in% c("B66","WCM249_3")))
```

    ## `summarise()` regrouping output by 'Sample.ID' (override with `.groups` argument)

``` r
tcga_rbind <- rbind(impact2, breast, uterine, colorectal, glioma, lung, skin, prostate, bladder, renal, esophagus)

breast_table <- data.frame(table((tcga_rbind %>% filter(type == "breast"))$variant))
uterine_table <- data.frame(table((tcga_rbind %>% filter(type == "uterine"))$variant))
colorectal_table <- data.frame(table((tcga_rbind %>% filter(type == "colorectal"))$variant))
lung_table <- data.frame(table((tcga_rbind %>% filter(type == "lung"))$variant))
skin_table <- data.frame(table((tcga_rbind %>% filter(type == "skin"))$variant))
glioma_table <- data.frame(table((tcga_rbind %>% filter(type == "glioma"))$variant))
prostate_table <- data.frame(table((tcga_rbind %>% filter(type == "prostate"))$variant))
bladder_table <- data.frame(table((tcga_rbind %>% filter(type == "bladder"))$variant))
renal_table <- data.frame(table((tcga_rbind %>% filter(type == "renal"))$variant))
esophagus_table <- data.frame(table((tcga_rbind %>% filter(type == "esophagus"))$variant))

tcga_merge <- merge(data.frame("variant" = breast_table$Var1, "breast" = breast_table$Freq),
                    data.frame("variant" = uterine_table$Var1, "uterine" = uterine_table$Freq), by = "variant",all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = colorectal_table$Var1, "colorectal" = colorectal_table$Freq), by = "variant", all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = lung_table$Var1, "lung" = lung_table$Freq), by = "variant", all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = skin_table$Var1, "skin" = skin_table$Freq), by = "variant", all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = glioma_table$Var1, "glioma" = glioma_table$Freq), by = "variant", all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = prostate_table$Var1, "prostate" = prostate_table$Freq), by = "variant", all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = bladder_table$Var1, "bladder" = bladder_table$Freq), by = "variant", all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = renal_table$Var1, "renal" = renal_table$Freq), by = "variant", all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = esophagus_table$Var1, "esophagus" = esophagus_table$Freq), by = "variant", all = T)
```

``` r
complete_abund_act2 <- complete_abund_act %>% filter(snv == 1) %>% mutate(position = gsub("[A-Z]","",variant) ,end = substr(gsub("[0-9]","",variant),2,2)) %>% mutate(abund_act_class = as.character(abund_act_class))
complete_abund_act2[complete_abund_act2$position %in% seq(1,350,1) & complete_abund_act2$end == "X","abund_act_class"] <- "3_unstable_inactive"

abund_act_tcga <- merge(complete_abund_act2[,c("variant","abund_act_class")],tcga_merge, by = "variant", all = T) %>% mutate(count = 1)
abund_act_tcga[abund_act_tcga$variant %in% c("T319X","Y68H","L152X","V53X","M198X","F104X","V343X","L108X","D109X","F258X","F341X","H93X"),"abund_act_class"] <- "3_unstable_inactive"
abund_act_tcga[is.na(abund_act_tcga)] <- 0
abund_act_tcga[abund_act_tcga$abund_act_class == 0,"abund_act_class"] <- "NA"

abund_act_tcga_summary <- abund_act_tcga %>% group_by(abund_act_class) %>% summarize(possible = sum(count), breast = sum(breast), uterine = sum(uterine), colorectal = sum(colorectal), lung = sum(lung), skin = sum(skin), glioma = sum(glioma), prostate = sum(prostate), bladder = sum(bladder), renal = sum(renal), esophagus = sum(esophagus))
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

``` r
abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)] <- t(t(abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)]) / colSums(abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)]))
colSums(abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)])
```

    ##   possible     breast    uterine colorectal       lung       skin     glioma 
    ##          1          1          1          1          1          1          1 
    ##   prostate    bladder      renal  esophagus 
    ##          1          1          1          1

``` r
abund_act_tcga_summary2 <- abund_act_tcga_summary %>%  filter(abund_act_class != "NA") 

abund_act_tcga_summary_melt <- melt(as.data.frame(abund_act_tcga_summary2), id = "abund_act_class") %>% filter(variable %in% c("possible","breast","uterine","lung","glioma","skin","renal"))

Cancer_genomics_plot1.pdf = ggplot() + 
  theme_bw() + 
  theme(panel.grid.major.x = element_blank(), axis.text.x = element_text(angle = 0, hjust = 0, vjust = 0.5)) +
  xlab(NULL) + ylab("Fraction of observed variants") +
  scale_y_log10(limits = c(0.001,1)) +
  geom_hline(yintercept = 1, linetype = 2) +
  geom_point(data = subset(abund_act_tcga_summary_melt, variable != "possible"), aes(x = abund_act_class, y = value, color = variable), position=position_dodge(width=0.7), alpha = 1) +
  geom_point(data = subset(abund_act_tcga_summary_melt, variable == "possible"), aes(x = abund_act_class, y = value), shape = 95, size = 30, alpha = 0.5)
Cancer_genomics_plot1.pdf
```

![](PTEN_composite_analysis_files/figure-gfm/TCGA%20plot-1.png)<!-- -->

``` r
ggsave(file = "plots/Cancer_genomics_plot1.pdf", Cancer_genomics_plot1.pdf, height = 40, width = 120, units = "mm")
```

``` r
complete_abund_act2 <- complete_abund_act %>% filter(snv == 1) %>% mutate(position = gsub("[A-Z]","",variant) ,end = substr(gsub("[0-9]","",variant),2,2)) %>% mutate(abund_act_class = as.character(abund_act_class))
complete_abund_act2[complete_abund_act2$variant %in% c("R130G","G129E","R130Q","C124S"),"abund_act_class"] <- "5_known_dominant_negative"
complete_abund_act2[complete_abund_act2$variant %in% c("P38S","D92H","R130P"),"abund_act_class"] <- "6_novel_dominant_negative"
complete_abund_act2[complete_abund_act2$position %in% seq(1,350,1) & complete_abund_act2$end == "X","abund_act_class"] <- "3_unstable_inactive"

abund_act_tcga <- merge(complete_abund_act2[,c("variant","abund_act_class")],tcga_merge, by = "variant", all = T) %>% mutate(count = 1)
abund_act_tcga[abund_act_tcga$variant %in% c("T319X","Y68H","L152X","V53X","M198X","F104X","V343X","L108X","D109X","F258X","F341X","H93X"),"abund_act_class"] <- "3_unstable_inactive"
abund_act_tcga[is.na(abund_act_tcga)] <- 0
abund_act_tcga[abund_act_tcga$abund_act_class == 0,"abund_act_class"] <- "NA"

abund_act_tcga_summary <- abund_act_tcga %>% group_by(abund_act_class) %>% summarize(possible = sum(count), breast = sum(breast), uterine = sum(uterine), colorectal = sum(colorectal), lung = sum(lung), skin = sum(skin), glioma = sum(glioma), prostate = sum(prostate), bladder = sum(bladder), renal = sum(renal), esophagus = sum(esophagus))
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

``` r
abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)] <- t(t(abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)]) / colSums(abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)]))
colSums(abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)])
```

    ##   possible     breast    uterine colorectal       lung       skin     glioma 
    ##          1          1          1          1          1          1          1 
    ##   prostate    bladder      renal  esophagus 
    ##          1          1          1          1

``` r
abund_act_tcga_summary2 <- abund_act_tcga_summary %>%  filter(abund_act_class %in% c("4_stable_inactive","5_known_dominant_negative","6_novel_dominant_negative"))

abund_act_tcga_summary_melt <- melt(as.data.frame(abund_act_tcga_summary2), id = "abund_act_class") %>% filter(variable %in% c("possible","breast","uterine","lung","glioma","skin","renal"))

Cancer_genomics_plot2.pdf = ggplot() + 
  theme_bw() + 
  theme(panel.grid.major.x = element_blank(), axis.text.x = element_text(angle = 0, hjust = 0, vjust = 0.5)) +
  xlab(NULL) + ylab("Fraction of observed variants") +
  scale_y_log10(limits = c(0.001,1)) +
  geom_hline(yintercept = 1, linetype = 2) +
  geom_point(data = subset(abund_act_tcga_summary_melt, variable != "possible"), aes(x = abund_act_class, y = value, color = variable), position=position_dodge(width=0.7), alpha = 1) +
  geom_point(data = subset(abund_act_tcga_summary_melt, variable == "possible"), aes(x = abund_act_class, y = value), shape = 95, size = 30, alpha = 0.5)
Cancer_genomics_plot2.pdf
```

    ## Warning: Transformation introduced infinite values in continuous y-axis

![](PTEN_composite_analysis_files/figure-gfm/Now%20combine%20all%20of%20the%20above-1.png)<!-- -->

``` r
ggsave(file = "plots/Cancer_genomics_plot2.pdf", Cancer_genomics_plot2.pdf, height = 40, width = 80, units = "mm")
```

    ## Warning: Transformation introduced infinite values in continuous y-axis

``` r
stable_inactive_tcga <- abund_act_tcga %>% arrange(desc(breast, uterine))
stable_inactive_to_test <- complete_abund_act_missense %>% filter(variant %in% c("R130P","D92H","D24G","R159S","Y46D","Y16S","T160P"))
stable_inactive_to_test2 <- merge(stable_inactive_to_test, stable_inactive_tcga[,c("variant","breast","uterine")], by = "variant", all.x = T)
```

``` r
western_blotting <- read.csv(file = "input_datatables/Western_blotting_summary.csv", header = T, stringsAsFactors = F)

blotting_figure_height <- 35
blotting_figure_width <- 70

pakt <- western_blotting[,c("label","pakt_1","pakt_2","pakt_3")]
# Divide each data column by the no intensity value
for(x in 2:ncol(pakt)){pakt[,x] <- pakt[,x] / pakt[1,x]}
pakt_melted <- melt(pakt, id = "label")
pakt$mean <- apply(pakt[,c("pakt_1", "pakt_2", "pakt_3")], 1, mean)
pakt$sd <- apply(pakt[,c("pakt_1", "pakt_2", "pakt_3")], 1, sd)
pakt$label <- factor(pakt$label, levels = pakt$label)
pakt_western_plot <- ggplot() + 
  theme(panel.grid.major.x = element_blank(), axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5)) +
  xlab(NULL) + ylab("Normalized\nintensity\npT308 Akt1") +
  geom_point(data = pakt, aes(x = label, y = mean), shape = 95, size = 6) + 
  geom_point(data = pakt_melted, aes(x = label, y = value), size = 1, alpha = 0.3) + 
  scale_y_log10(limits = c(0.05,50))
ggsave(file = "Plots/Western_plot_pAKT.pdf", pakt_western_plot, height = blotting_figure_height, width = blotting_figure_width, units = "mm")

akt <- western_blotting[,c("label","akt_1","akt_2","akt_3")]
# Divide each data column by the no intensity value
for(x in 2:ncol(akt)){akt[,x] <- akt[,x] / akt[1,x]}
akt_melted <- melt(akt, id = "label")
akt$mean <- apply(akt[,c("akt_1", "akt_2", "akt_3")], 1, mean)
akt$sd <- apply(akt[,c("akt_1", "akt_2", "akt_3")], 1, sd)
akt$label <- factor(akt$label, levels = akt$label)
akt_western_plot <- ggplot() + 
  theme(panel.grid.major.x = element_blank(), axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5)) +
  xlab(NULL) + ylab("Normalized\nintensity\nall Akt") +
  geom_point(data = akt, aes(x = label, y = mean), shape = 95, size = 6) + 
  geom_point(data = akt_melted, aes(x = label, y = value), size = 1, alpha = 0.3) + 
  scale_y_log10(limits = c(0.05,50))
ggsave(file = "Plots/Western_plot_panAKT.pdf", akt_western_plot, height = blotting_figure_height, width = blotting_figure_width, units = "mm")

ha <- western_blotting[,c("label","ha_1","ha_2","ha_3")]
# Divide each data column by the WT protein intensity value
for(x in 2:ncol(ha)){ha[,x] <- ha[,x] / ha[2,x]}
ha_melted <- melt(ha, id = "label")
ha$mean <- apply(ha[,c("ha_1", "ha_2", "ha_3")], 1, mean)
ha$sd <- apply(ha[,c("ha_1", "ha_2", "ha_3")], 1, sd)
ha$label <- factor(ha$label, levels = ha$label)
ha_western_plot <- ggplot() + 
  theme(panel.grid.major.x = element_blank(), axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5)) +
  xlab(NULL) + ylab("Normalized\nintensity\nHA-PTEN") +
  geom_point(data = ha, aes(x = label, y = mean), shape = 95, size = 6) + 
  geom_point(data = ha_melted, aes(x = label, y = value), size = 1, alpha = 0.3) + 
  scale_y_log10(limits = c(0.05,50))
ggsave(file = "Plots/Western_plot_ha.pdf", ha_western_plot, height = blotting_figure_height, width = blotting_figure_width, units = "mm")
```

    ## Warning: Removed 1 rows containing missing values (geom_point).

    ## Warning: Removed 2 rows containing missing values (geom_point).

``` r
actin <- western_blotting[,c("label","actin_1","actin_2","actin_3")]
# Divide each data column by the WT protein intensity value
for(x in 2:ncol(actin)){actin[,x] <- actin[,x] / actin[2,x]}
actin_melted <- melt(actin, id = "label")
actin$mean <- apply(actin[,c("actin_1", "actin_2", "actin_3")], 1, mean)
actin$sd <- apply(actin[,c("actin_1", "actin_2", "actin_3")], 1, sd)
actin$label <- factor(actin$label, levels = actin$label)
actin_western_plot <- ggplot() + 
  theme(panel.grid.major.x = element_blank(), axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5)) +
  xlab(NULL) + ylab("Normalized\nintensity\nbeta-actin") +
  geom_point(data = actin, aes(x = label, y = mean), shape = 95, size = 6) + 
  geom_point(data = actin_melted, aes(x = label, y = value), size = 1, alpha = 0.3) + 
  scale_y_log10(limits = c(0.05,50))
ggsave(file = "plots/Western_plot_actin.pdf", actin_western_plot, height = blotting_figure_height, width = blotting_figure_width, units = "mm")
```

``` r
pakt_for_merge <- pakt[,c("label","mean")]
colnames(pakt_for_merge) <- c("variant","pakt")

tcga_merge_total_count <- tcga_merge
tcga_merge_total_count$total_cancer_count <- rowSums(tcga_merge_total_count[,colnames(tcga_merge_total_count)[(!(colnames(tcga_merge_total_count) %in% "variant"))]], na.rm = T)

pakt_merged <- merge(pakt_for_merge, tcga_merge_total_count[,c("variant","total_cancer_count")], all.x = T)

pakt_merged[is.na(pakt_merged)] <- 0

pAkt_vs_TCGA_count_plot <- ggplot() + 
  theme_bw() +
  geom_text_repel(data = subset(pakt_merged, !(variant %in% c("WT","none"))), aes(x = pakt, y = total_cancer_count, label = variant), color = "red", segment.colour = "orange") +
  geom_point(data = subset(pakt_merged, !(variant %in% c("WT","none"))), aes(x = pakt, y = total_cancer_count)) +
  xlab("Normalized Akt1 pT308 by western blot") + 
  ylab("Total number of variants observed in TCGA") +
  scale_x_log10(limits = c(0.5,12.5)) +
  geom_vline(xintercept = 1, linetype = 2, alpha = 0.5) +
  geom_vline(xintercept = 0.5252194, linetype = 2, alpha = 0.5, color = "blue")
pAkt_vs_TCGA_count_plot
```

![](PTEN_composite_analysis_files/figure-gfm/pAKT%20vs%20cancer%20counts-1.png)<!-- -->

``` r
ggsave(file = "plots/pAkt_vs_TCGA_count_plot.pdf", pAkt_vs_TCGA_count_plot, height = 60, width = 100, units = "mm")

paste("The Pearson's r of the TCGA variant count and pAKT level scored in our western blot:",round(cor(pakt_merged$pakt, pakt_merged$total_cancer_count, method = "pearson"),2))
```

    ## [1] "The Pearson's r of the TCGA variant count and pAKT level scored in our western blot: 0.77"

``` r
ccle_muts <- read.csv(file = "input_datatables/CCLE_PTEN_mutations.csv", header = T, stringsAsFactors = FALSE)
ccle_rppa <- read.csv(file = "input_datatables/CCLE_RPPA_20181003.csv", header = T, stringsAsFactors = FALSE)

colnames(ccle_rppa)
```

    ##   [1] "X"                                "X14.3.3_beta"                    
    ##   [3] "X14.3.3_epsilon_Caution"          "X14.3.3_zeta"                    
    ##   [5] "X4E.BP1"                          "X4E.BP1_pS65"                    
    ##   [7] "X4E.BP1_pT37_T46"                 "X4E.BP1_pT70"                    
    ##   [9] "X53BP1"                           "A.Raf_pS299_Caution"             
    ##  [11] "ACC_pS79"                         "ACC1_Caution"                    
    ##  [13] "Acetyl.a.Tubulin..Lys40._Caution" "ACVRL1_Caution"                  
    ##  [15] "ADAR1"                            "Akt"                             
    ##  [17] "Akt_pS473"                        "Akt_pT308"                       
    ##  [19] "alpha.Catenin"                    "AMPK_alpha_Caution"              
    ##  [21] "AMPK_pT172"                       "Annexin.1"                       
    ##  [23] "Annexin_VII"                      "AR"                              
    ##  [25] "ASNS"                             "ATM"                             
    ##  [27] "B.Raf_Caution"                    "B.Raf_pS445"                     
    ##  [29] "Bad_pS112"                        "Bak_Caution"                     
    ##  [31] "Bap1.c.4"                         "Bax"                             
    ##  [33] "Bcl.2"                            "Bcl.xL"                          
    ##  [35] "Beclin_Caution"                   "beta.Catenin"                    
    ##  [37] "beta.Catenin_pT41_S45"            "beta.Actin_Caution"              
    ##  [39] "Bid_Caution"                      "Bim.CST2933."                    
    ##  [41] "Bim.EP1036."                      "BRCA2_Caution"                   
    ##  [43] "c.Jun_pS73"                       "c.Kit"                           
    ##  [45] "c.Met_Caution"                    "c.Met_pY1235"                    
    ##  [47] "c.Myc_Caution"                    "C.Raf.BD610151._Caution"         
    ##  [49] "C.Raf.MP05.739."                  "C.Raf_pS338"                     
    ##  [51] "Caspase.7_cleavedD198_Caution"    "Caspase.8_Caution"               
    ##  [53] "Caveolin.1"                       "CD20._Caution"                   
    ##  [55] "CD31"                             "CD49b"                           
    ##  [57] "CDK1"                             "Chk1_Caution"                    
    ##  [59] "Chk1_pS345_Caution"               "Chk2"                            
    ##  [61] "Chk2_pT68_Caution"                "cIAP_Caution"                    
    ##  [63] "Claudin.7"                        "Collagen_VI"                     
    ##  [65] "Cyclin_B1"                        "Cyclin_D1"                       
    ##  [67] "Cyclin_E1"                        "Cyclin_E2_Caution"               
    ##  [69] "Di.Ras3_Caution"                  "DJ.1"                            
    ##  [71] "Dvl3"                             "E.Cadherin"                      
    ##  [73] "eEF2_Caution"                     "eEF2K"                           
    ##  [75] "EGFR"                             "EGFR_pY1068_Caution"             
    ##  [77] "EGFR_pY1173"                      "eIF4E"                           
    ##  [79] "eIF4G_Caution"                    "ER.alpha"                        
    ##  [81] "ER.alpha_pS118"                   "ERCC1_Caution"                   
    ##  [83] "ERK2_Caution"                     "ETS.1"                           
    ##  [85] "FASN"                             "Fibronectin"                     
    ##  [87] "FoxM1"                            "FOXO3a_Caution"                  
    ##  [89] "FOXO3a_pS318_S321_Caution"        "FRA1_Caution"                    
    ##  [91] "G6PD"                             "Gab2"                            
    ##  [93] "GAPDH_Caution"                    "GATA3"                           
    ##  [95] "GSK.3.BETA_Caution"               "GSK3.alpha.beta"                 
    ##  [97] "GSK3.alpha.beta_pS21_S9"          "GSK3_pS9"                        
    ##  [99] "HER2"                             "HER2_pY1248_Caution"             
    ## [101] "HER3"                             "HER3_pY1289_Caution"             
    ## [103] "Heregulin"                        "HSP70_Caution"                   
    ## [105] "IGFBP2"                           "INPP4B"                          
    ## [107] "IRS1"                             "JAK2"                            
    ## [109] "JNK_pT183_Y185"                   "JNK2_Caution"                    
    ## [111] "Ku80_Caution"                     "Lck"                             
    ## [113] "MAPK_pT202_Y204"                  "MDM2_pS166"                      
    ## [115] "MDMX_MDM4.BetIHC.00108._Caution"  "MEK1"                            
    ## [117] "MEK1_pS217_S221"                  "MIG.6"                           
    ## [119] "Mre11_Caution"                    "MSH2"                            
    ## [121] "MSH6_Caution"                     "mTOR"                            
    ## [123] "mTOR_pS2448_Caution"              "MYH11"                           
    ## [125] "Myosin.IIa.pS1943"                "N.Cadherin"                      
    ## [127] "N.Ras"                            "NDRG1_pT346"                     
    ## [129] "NF.kB.p65_pS536_Caution"          "NF2_Caution"                     
    ## [131] "Notch1"                           "P.Cadherin_Caution"              
    ## [133] "p14.Arf.BetA300.340A._Caution"    "p21"                             
    ## [135] "p27"                              "p27_pT157_Caution"               
    ## [137] "p27_pT198"                        "p38.alpha.MAPK"                  
    ## [139] "p38_MAPK"                         "p38_pT180_Y182"                  
    ## [141] "p53_Caution"                      "p62.Lck.ligand_Caution"          
    ## [143] "p70S6K"                           "p70S6K_pT389"                    
    ## [145] "p90RSK_Caution"                   "p90RSK_pT359_S363_Caution"       
    ## [147] "p90RSK_pT573_Caution"             "PAI.1"                           
    ## [149] "PARP_cleaved_Caution"             "Paxillin_Caution"                
    ## [151] "PCNA_Caution"                     "PDCD4_Caution"                   
    ## [153] "PDK1"                             "PDK1_pS241"                      
    ## [155] "PEA15"                            "PEA15_pS116"                     
    ## [157] "PI3K.p110.alpha_Caution"          "PI3K.p85"                        
    ## [159] "PKC.alpha"                        "PKC.alpha_pS657_Caution"         
    ## [161] "PKC.delta_pS664"                  "PKC.pan_BetaII_pS660"            
    ## [163] "Porin"                            "PR"                              
    ## [165] "PRAS40_pT246"                     "PRDX1"                           
    ## [167] "PREX1"                            "PTEN"                            
    ## [169] "Rab25"                            "Rad50"                           
    ## [171] "RAD51"                            "Raptor"                          
    ## [173] "Rb_Caution"                       "Rb_pS807_S811"                   
    ## [175] "RBM15"                            "Rictor_Caution"                  
    ## [177] "Rictor_pT1135"                    "RSK1.2.3_Caution"                
    ## [179] "S6_pS235_S236"                    "S6_pS240_S244"                   
    ## [181] "SCD1"                             "SETD2_Caution"                   
    ## [183] "SF2"                              "Shc_pY317"                       
    ## [185] "SHP.2_pY542_Caution"              "Smac_Caution"                    
    ## [187] "Smad1"                            "Smad3"                           
    ## [189] "Smad4"                            "Snail_Caution"                   
    ## [191] "Src"                              "Src_pY416_Caution"               
    ## [193] "Src_pY527"                        "STAT3_Caution"                   
    ## [195] "STAT3_pY705"                      "STAT5.alpha"                     
    ## [197] "Stathmin"                         "Syk"                             
    ## [199] "TAZ"                              "TFRC"                            
    ## [201] "TIGAR"                            "Transglutaminase"                
    ## [203] "TSC1_Caution"                     "TTF1"                            
    ## [205] "Tuberin"                          "Tuberin_pT1462"                  
    ## [207] "VAV1_Caution"                     "VEGFR2"                          
    ## [209] "VHL_Caution"                      "XBP1_Caution"                    
    ## [211] "XRCC1_Caution"                    "YAP_Caution"                     
    ## [213] "YAP_pS127_Caution"                "YB.1"                            
    ## [215] "YB.1_pS102"

``` r
ccle_short <- ccle_rppa[,c("X","Akt_pT308","PTEN")]
for(x in 1:nrow(ccle_short)){
  ccle_short$Cell.Line[x] <- strsplit(ccle_short$X[x], "_")[[1]][1]
}

ccle_muts_missense <- ccle_muts %>% filter(Variant.Classification == "Missense_Mutation") 
ccle_muts_missense_single <- ccle_muts_missense %>% mutate(number = 1) %>% group_by(Cell.Line) %>% summarize(number = sum(number)) %>% filter(number == 1)
```

    ## `summarise()` ungrouping output (override with `.groups` argument)

``` r
ccle_muts_missense_final <- merge(ccle_muts_missense, ccle_muts_missense_single, by = "Cell.Line")

ccle_merged<- merge(ccle_muts_missense_final, ccle_short, by = "Cell.Line")

ccle_merged$variant <- substr(ccle_merged$Protein.Change,3,15)


list_of_dominant_negatives <- c("C124S","R130G","R130Q","P38S","G129E","R130P","D92H")
list_to_highlight <- c("C124S","R130G","R130Q","P38S","G129E","R130P","D92H", "L42R")

custom_colorscale <- c("C124S" = "red","R130G" = "red","R130Q" = "red","P38S" = "red","G129E" = "red","R130P" = "red","D92H" = "red", "L42R" = "blue")

PTEN_vs_pAkt_in_CCLE <- ggplot() + 
  theme(legend.position = "none") + 
  geom_text_repel(data = subset(ccle_merged, variant %in% list_to_highlight), aes(x = PTEN, y = Akt_pT308, label = variant, color = variant), segment.colour = "grey50") +
  geom_point(data = ccle_merged, aes(x = PTEN, y = Akt_pT308)) +
  geom_point(data = subset(ccle_merged, variant %in% list_of_dominant_negatives), aes(x = PTEN, y = Akt_pT308), color = "red", size = 0.8) +
  xlab("PTEN protein level in CCLE") + ylab("Akt1 pT308 protein level in CCLE") +
  scale_color_manual(values = custom_colorscale)
PTEN_vs_pAkt_in_CCLE
```

![](PTEN_composite_analysis_files/figure-gfm/Dominant%20negatives%20in%20CCLE-1.png)<!-- -->

``` r
ggsave(file = "plots/PTEN_vs_pAkt_in_CCLE.pdf", PTEN_vs_pAkt_in_CCLE, height = 65, width = 100, units = "mm")
```