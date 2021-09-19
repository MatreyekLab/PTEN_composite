# PTEN_composite
PTEN fill-in abundance DMS and integration with yeast activity scores

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

    ## ggtree v3.0.2  For help: https://yulab-smu.top/treedata-book/
    ## 
    ## If you use ggtree in published research, please cite the most appropriate paper(s):
    ## 
    ## 1. Guangchuang Yu. Using ggtree to visualize data on tree-like structures. Current Protocols in Bioinformatics, 2020, 69:e96. doi:10.1002/cpbi.96
    ## 2. Guangchuang Yu, Tommy Tsan-Yuk Lam, Huachen Zhu, Yi Guan. Two methods for mapping and visualizing associated data on phylogeny using ggtree. Molecular Biology and Evolution 2018, 35(12):3041-3043. doi:10.1093/molbev/msy194
    ## 3. Guangchuang Yu, David Smith, Huachen Zhu, Yi Guan, Tommy Tsan-Yuk Lam. ggtree: an R package for visualization and annotation of phylogenetic trees with their covariates and other associated data. Methods in Ecology and Evolution 2017, 8(1):28-36. doi:10.1111/2041-210X.12628

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

    ## ── Attaching packages ─────────────────────────────────────── tidyverse 1.3.1 ──

    ## ✓ tibble  3.1.4     ✓ dplyr   1.0.7
    ## ✓ tidyr   1.1.3     ✓ stringr 1.4.0
    ## ✓ readr   2.0.1     ✓ forcats 0.5.1
    ## ✓ purrr   0.3.4

    ## ── Conflicts ────────────────────────────────────────── tidyverse_conflicts() ──
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
#if(!require(phytools)){install.packages("phytools")}
#library(phytools)


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

# Looking at the total number of barcodes in this secondary library

``` r
plasmid1 <- read.delim(file = "enrich2_output/Plasmid_1.tsv", sep = "\t"); colnames(plasmid1) <- c("barcode","count1")
plasmid2 <- read.delim(file = "enrich2_output/Plasmid_2.tsv", sep = "\t"); colnames(plasmid2) <- c("barcode","count2")
plasmid <- merge(plasmid1, plasmid2, by = "barcode", all = T)
plasmid[is.na(plasmid)] <- 0

plasmid$total <- plasmid$count1 + plasmid$count2

plasmid_barcodes <- plasmid %>% filter(total >= 20)
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
PTEN_subassembly_maps <- read.csv(file = "input_datatables/PTEN_subassembly_maps.csv", header = T, stringsAsFactors = F)

original <- subset(PTEN_subassembly_maps, library == "original")
fillin <- subset(PTEN_subassembly_maps, library == "fillin")

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

combined_variants$end <- factor(combined_variants$end, levels = c("G","S","T","C","A","M","W","Y","F","L","I","V","D","E","N","Q","H","K","R","P","X"))

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

    ## `summarise()` has grouped output by 'position'. You can override using the `.groups` argument.

``` r
#combined_variants2$library <- factor(combined_variants2$library, levels = c("fillin","original","both"))
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
colnames(original)[colnames(original) %in% c("abundance_class","score","sd","expts","se","lower_ci","upper_ci","egfp_geomean")] <- c("abundance_class_orig","score_orig","sd_orig","count_orig","se_orig","lower_ci_orig","upper_ci_orig","egfp_geomean")

# Rename the score for the original dataset
colnames(original)[colnames(original) == "score"] <- "score_orig"

## Import the fill-in dataset
replicates <- read.csv(file = "output_datatables/PTEN_fillin_vampseq_combined.csv", header =  TRUE, stringsAsFactors = FALSE)
colnames(replicates)[colnames(replicates) %in% c("e1s1","e1s2","e1s3","e1s4","e3s1","e3s2","e3s3","average","count","sd","se","lower_ci","upper_ci","abundance_class")] <- c("score9","score10","score11","score12","score13","score14","score15","score_fillin","count_fillin","sd_fillin","se_fillin","lower_ci_fillin","upper_ci_fillin","abundance_class_fillin")

combined <- merge(
  replicates[,c("variant","score9","score10","score11","score12","score13","score14","score15","score_fillin","count_fillin","sd_fillin","se_fillin","lower_ci_fillin","upper_ci_fillin","abundance_class_fillin")], 
  original[,c("variant","position","start","end","class","snv","score_orig","abundance_class_orig","sd_orig","count_orig","se_orig","lower_ci_orig","upper_ci_orig","egfp_geomean","score1","score2","score3","score4","score5","score6","score7","score8")],
  by = "variant", all = T)

combined <- combined[,c("variant","position","start","end","class","snv","egfp_geomean","score_orig","abundance_class_orig","score_fillin","score1","score2","score3","score4","score5","score6","score7","score8","score9","score10","score11","score12","score13","score14","score15","sd_orig","count_orig","se_orig","lower_ci_orig","upper_ci_orig","sd_fillin","count_fillin","se_fillin","lower_ci_fillin","upper_ci_fillin")]
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
paste("Number of positions where 18 or more missense variants were scored in the first paper:", sum(data.frame(table((combined %>% filter(class == "missense", !is.na(score_orig) & variant != "M1V"))$position))$Freq >= 17))
```

    ## [1] "Number of positions where 18 or more missense variants were scored in the first paper: 50"

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
  geom_point(data = combined_5plus, aes(x = score_orig, y = score_fillin), alpha = 0.5) +
  geom_text(aes(x = 0, y = 1.2, label = paste("n=",nrow(combined_5plus))))
Experiment_score_correlation_plot.pdf
```

![](PTEN_composite_analysis_files/figure-gfm/Compare%20between%20the%20two%20datasets-1.png)<!-- -->

``` r
ggsave(file = "plots/Experiment_score_correlation_plot.pdf", Experiment_score_correlation_plot.pdf, height = 50, width = 80, units = "mm")

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

# Creating a schematic that will help in describing the replicate filtering scheme in a supplementary figure

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
  observed_frame$called_incorrectly <- 0
  
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
    observed_frame$called_incorrectly[x] <- called_incorrectly
    
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

observed_frame$pct_correct_of_total_nonsense <- observed_frame$called_correctly / (observed_frame$called_correctly + observed_frame$called_incorrectly) * 100

correct_and_incorrectly_scored_plot <- ggplot() + 
  theme_bw() + 
  theme(panel.grid.major.x = element_blank()) +
  labs(x = "Minimum variant replicate\ncount for inclusion", y = "Correctly(green) or\nincorrectly(red) scored") +
  scale_x_continuous(limits = c(0,15), breaks = c(0,5,10,15)) +
  geom_hline(yintercept = 0, alpha = 0.5) +
  geom_line(data = observed_frame, aes(x = cutoff_inclusive, y = called_correctly), alpha = 0.5, width = 0.2, color = "dark green") +
  geom_point(data = observed_frame, aes(x = cutoff_inclusive, y = called_correctly), alpha = 0.5, width = 0.2, color = "dark green") +
  geom_text(data = observed_frame, aes(x = cutoff_inclusive, y = called_correctly+10, label = called_correctly), alpha = 1, color = "dark green", size = 2.5) +
  geom_line(data = observed_frame, aes(x = cutoff_inclusive, y = called_incorrectly), alpha = 0.5, width = 0.2, color = "magenta") +
  geom_point(data = observed_frame, aes(x = cutoff_inclusive, y = called_incorrectly), alpha = 0.5, width = 0.2, color = "magenta") +
  geom_text(data = observed_frame, aes(x = cutoff_inclusive, y = called_incorrectly-15, label = called_incorrectly), alpha = 1, color = "magenta", size = 2.5)
correct_and_incorrectly_scored_plot
```

![](PTEN_composite_analysis_files/figure-gfm/Optimizing%20replicate%20numbers-1.png)<!-- -->

``` r
ggsave(file = "Plots/Correct_and_incorrectly_scored_plot.pdf", correct_and_incorrectly_scored_plot, height = 50, width = 80, units = "mm")

replicate_cutoff_nonsense_syn_plot <- ggplot() + 
  theme_bw() + 
  theme(panel.grid.major.x = element_blank()) +
  scale_x_continuous(limits = c(0,15), breaks = c(0,5,10,15)) +
  labs(x = "Minimum variant replicate\ncount for inclusion", y = "Nonsense variants correctly\nscored over random") +
  geom_jitter(data = summary_frame_melted, aes(x = cutoff_inclusive, y = value), alpha = 0.1, width = 0.2) +
  geom_boxplot(data = summary_frame_melted, aes(x = cutoff_inclusive, y = value, group = cutoff_inclusive), alpha = 0.2, fill = "red")
replicate_cutoff_nonsense_syn_plot
```

![](PTEN_composite_analysis_files/figure-gfm/Optimizing%20replicate%20numbers-2.png)<!-- -->

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

syn_non_mis_hist_n_frame <- data.frame("n" = c(nrow(subset(combined_for_plotting_classes, plotting_group == "synonymous" & !is.na(score_abundance))),
                                               nrow(subset(combined_for_plotting_classes, plotting_group == "nonsense" & !is.na(score_abundance))),
                                               nrow(subset(combined_for_plotting_classes, plotting_group == "missense" & !is.na(score_abundance)))),
                                       "plotting_group" = c("synonymous","nonsense","missense"), "y" = c(15,20,300))

Synonymous_nonsense_missense_histograms_plot <- ggplot() + 
  theme_bw() + 
  theme(panel.grid.major.y = element_blank()) +
  xlab("Abundance score") + 
  geom_hline(yintercept = 0) +
  geom_histogram(data = combined_for_plotting_classes, aes(x = score_abundance), fill = "grey50", alpha = 0.5, color = "black") +
  geom_text(data = syn_non_mis_hist_n_frame, aes(x = 0.4, y = y, label = paste("n=",n)), hjust = 0.5) +
  facet_grid(rows = vars(plotting_group), scales = "free_y")
Synonymous_nonsense_missense_histograms_plot
```

    ## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.

    ## Warning: Removed 3436 rows containing non-finite values (stat_bin).

![](PTEN_composite_analysis_files/figure-gfm/Using%20above%20graph%20make%20the%20right%20dataset-1.png)<!-- -->

``` r
ggsave(file = "Plots/Synonymous_nonsense_missense_histograms_plot.pdf", Synonymous_nonsense_missense_histograms_plot, height = 50, width = 80, units = "mm")
```

    ## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.

    ## Warning: Removed 3436 rows containing non-finite values (stat_bin).

``` r
paste("We now have abundance scores for",
      nrow(subset(combined, class == "synonymous" & !is.na(score_abundance))),"synonymous variants")
```

    ## [1] "We now have abundance scores for 144 synonymous variants"

``` r
paste("We now have abundance scores for",
      nrow(subset(combined, class == "nonsense" & !is.na(score_abundance))),"nonsense variants")
```

    ## [1] "We now have abundance scores for 160 nonsense variants"

``` r
paste("We now have abundance scores for",
      nrow(subset(combined, class == "missense" & !is.na(score_abundance))),"missense variants")
```

    ## [1] "We now have abundance scores for 4387 missense variants"

# To see if the updated dataset is higher in quality, assess how the coefficient of variation changed for variants observed in both datasets

``` r
combined_for_plotting_classes_4plus_orig <- combined_for_plotting_classes %>% filter(count_orig >= 4 & score_orig >= -0.2 & score_total >= -0.2)
combined_for_plotting_classes_4plus_composite <- combined_for_plotting_classes %>% filter(count_total >= 4 & score_orig >= -0.2 & score_total >= -0.2)

combined_for_plotting_classes_4plus_orig$cv_orig <- combined_for_plotting_classes_4plus_orig$sd_orig / combined_for_plotting_classes_4plus_orig$score_orig
combined_for_plotting_classes_4plus_composite$cv_total <- combined_for_plotting_classes_4plus_composite$sd_total / combined_for_plotting_classes_4plus_composite$score_total

combined_for_plotting_classes_4plus_orig[combined_for_plotting_classes_4plus_orig$cv_orig < - 0.1,"cv_orig"] <- -0.2
combined_for_plotting_classes_4plus_composite[combined_for_plotting_classes_4plus_composite$cv_total < - 0.1,"cv_total"] <- -0.2

combined_for_plotting_classes_4plus_orig[combined_for_plotting_classes_4plus_orig$cv_orig > 1.5,"cv_orig"] <- 1.7
combined_for_plotting_classes_4plus_composite[combined_for_plotting_classes_4plus_composite$cv_total > 1.5,"cv_total"] <- 1.7

paste("fraction of original missense variants with CV < 0.5:",round(nrow(subset(combined_for_plotting_classes_4plus_orig, cv_orig > 0 & cv_orig < 0.5)) / nrow(combined_for_plotting_classes_4plus_orig),2))
```

    ## [1] "fraction of original missense variants with CV < 0.5: 0.76"

``` r
paste("fraction of total missense variants with CV < 0.5:",round(nrow(subset(combined_for_plotting_classes_4plus_composite, cv_total > 0 & cv_total < 0.5)) / nrow(combined_for_plotting_classes_4plus_composite),2))
```

    ## [1] "fraction of total missense variants with CV < 0.5: 0.78"

``` r
paste("fraction of original missense variants with CV > 1.5:",round(nrow(subset(combined_for_plotting_classes_4plus_orig, cv_orig > 0 & cv_orig > 1.5)) / nrow(combined_for_plotting_classes_4plus_orig),2))
```

    ## [1] "fraction of original missense variants with CV > 1.5: 0.02"

``` r
paste("fraction of total missense variants with CV > 1.5:",round(nrow(subset(combined_for_plotting_classes_4plus_composite, cv_total > 0 & cv_total > 1.5)) / nrow(combined_for_plotting_classes_4plus_composite),2))
```

    ## [1] "fraction of total missense variants with CV > 1.5: 0.01"

``` r
Coefficient_of_variation_plot <- 
ggplot() + theme_bw() + 
  scale_x_continuous(limits = c(-0.25,1.8)) +
  geom_histogram(data = combined_for_plotting_classes_4plus_orig, aes(x = cv_orig), fill = "blue", alpha = 0.5, color = "blue", binwidth = 0.05) +
  geom_histogram(data = combined_for_plotting_classes_4plus_composite, aes(x = cv_total), fill = "red", alpha = 0.5, color = "red", binwidth = 0.05) +
  geom_vline(xintercept = 0.5, linetype = 2, alpha = 0.4) + geom_vline(xintercept = 0, linetype = 2, alpha = 0.4) +
  ylab("Number of variants") + xlab("Coefficient of variation")
Coefficient_of_variation_plot
```

    ## Warning: Removed 2 rows containing missing values (geom_bar).

    ## Warning: Removed 2 rows containing missing values (geom_bar).

![](PTEN_composite_analysis_files/figure-gfm/Compare%20CV%20for%20variants%20we%20had%20seen%20before-1.png)<!-- -->

``` r
ggsave(file = "Plots/Coefficient_of_variation_plot.pdf", Coefficient_of_variation_plot, height = 40, width = 60, units = "mm")
```

    ## Warning: Removed 2 rows containing missing values (geom_bar).

    ## Warning: Removed 2 rows containing missing values (geom_bar).

``` r
cv_dataframe <- data.frame(dataset = c("Original","Composite"),
                           cv_below_pt5 = c(nrow(subset(combined_for_plotting_classes_4plus_orig, cv_orig > 0 & cv_orig < 0.5)),
                                            nrow(subset(combined_for_plotting_classes_4plus_composite, cv_total > 0 & cv_total < 0.5))))

cv_dataframe$dataset <- factor(cv_dataframe$dataset, levels = c("Original","Composite"))

low_cv_bargraph <- ggplot() + theme(panel.grid.major.x = element_blank()) + labs(x = NULL, y = "Number of variants") +
  scale_fill_manual(values = c("Original" = "blue", "Composite" = "red")) +
  geom_bar(data = cv_dataframe, aes(x = dataset, y = cv_below_pt5, fill = dataset), stat = "identity", alpha = 0.75, color = "black")
low_cv_bargraph
```

![](PTEN_composite_analysis_files/figure-gfm/Compare%20CV%20for%20variants%20we%20had%20seen%20before-2.png)<!-- -->

``` r
ggsave(file = "Plots/Low_CV_bargraph.pdf", low_cv_bargraph, height = 30, width = 60, units = "mm")

paste("There was a",round((cv_dataframe$cv_below_pt5[2] - cv_dataframe$cv_below_pt5[1]) / cv_dataframe$cv_below_pt5[1] * 100,1),"percent increase in the number of variants with a CV less than 0.5")
```

    ## [1] "There was a 12.5 percent increase in the number of variants with a CV less than 0.5"

``` r
lm_composite_abundance <- lm(combined_for_plotting_classes$score_abundance ~ log10(combined_for_plotting_classes$egfp_geomean))
round(cor(combined_for_plotting_classes$score_abundance, combined_for_plotting_classes$egfp_geomean, use = "complete", method = "spearman")^2,2)
```

    ## [1] 0.93

``` r
lm_orig_abundance <- lm(combined_for_plotting_classes$score_orig ~ log10(combined_for_plotting_classes$egfp_geomean))
round(cor(combined_for_plotting_classes$score_orig, combined_for_plotting_classes$egfp_geomean, use = "complete", method = "spearman")^2,2)
```

    ## [1] 0.93

``` r
ggplot() + labs(x = "Log10 of geometric mean of MFI", y = "Abundance score") +
  geom_abline(slope = lm_composite_abundance$coefficients[2], intercept = lm_composite_abundance$coefficients[1], alpha = 0.25, size = 2, color = "red") +
  geom_point(data = combined_for_plotting_classes_4plus_composite, aes(x = log10(egfp_geomean), y = score_abundance), color = "red", alpha = 0.5) +
  geom_abline(slope = lm_orig_abundance$coefficients[2], intercept = lm_orig_abundance$coefficients[1], alpha = 0.25, size = 2, color = "blue") +
  geom_point(data = combined_for_plotting_classes_4plus_orig, aes(x = log10(egfp_geomean), y = score_orig), color = "blue", alpha = 0.5)
```

    ## Warning: Removed 3907 rows containing missing values (geom_point).

    ## Warning: Removed 3559 rows containing missing values (geom_point).

![](PTEN_composite_analysis_files/figure-gfm/Seeing%20if%20the%20new%20data%20makes%20the%20old%20individually%20characterized%20variant%20correlations%20better-1.png)<!-- -->

``` r
round(cor(combined_for_plotting_classes$score_orig, combined_for_plotting_classes$egfp_geomean, use = "complete", method = "spearman")^2,2)
```

    ## [1] 0.93

``` r
round(cor(combined_for_plotting_classes$score_abundance, combined_for_plotting_classes$egfp_geomean, use = "complete", method = "spearman")^2,2)
```

    ## [1] 0.93

``` r
Scores_vs_individually_assessed_variants_plot <- ggplot() + labs(x = "Mean fluorescence intensity of\nindividually tested variants", y = "Abundance score") +
  geom_point(data = combined_for_plotting_classes_4plus_orig, aes(x = egfp_geomean, y = score_orig), color = "blue", alpha = 0.5) +
  geom_point(data = combined_for_plotting_classes_4plus_composite, aes(x = egfp_geomean, y = score_abundance), color = "red", alpha = 0.5) +
  geom_text(aes(x = 1.6, y = 0.2, label = paste("Spearman's rho^2, original:",round(cor(combined_for_plotting_classes$score_orig, combined_for_plotting_classes$egfp_geomean, use = "complete", method = "spearman")^2,2))), hjust = 1, color = "blue", size = 2.75) +
  geom_text(aes(x = 1.6, y = 0, label = paste("Spearman's rho^2, composite:",round(cor(combined_for_plotting_classes$score_abundance, combined_for_plotting_classes$egfp_geomean, use = "complete", method = "spearman")^2,2))), hjust = 1, color = "red", size = 2.75)
Scores_vs_individually_assessed_variants_plot
```

    ## Warning: Removed 3559 rows containing missing values (geom_point).

    ## Warning: Removed 3907 rows containing missing values (geom_point).

![](PTEN_composite_analysis_files/figure-gfm/Seeing%20if%20the%20new%20data%20makes%20the%20old%20individually%20characterized%20variant%20correlations%20better-2.png)<!-- -->

``` r
ggsave(file = "Plots/Scores_vs_individually_assessed_variants_plot.pdf", Scores_vs_individually_assessed_variants_plot, height = 40, width = 70, units = "mm")
```

    ## Warning: Removed 3559 rows containing missing values (geom_point).

    ## Warning: Removed 3907 rows containing missing values (geom_point).

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
unassigned_so_far <- subset(combined, !is.na(score_abundance) & !(class %in% c("synonymous","nonsense","missense")))
## Looks like a few synonymous variants were not classified that. Go back and do that now.
for(x in 1:nrow(combined)){
  if(is.na(combined$start[x])){
    combined$start[x] <- substr(gsub("[^A-Za-z]", "", combined$variant[x]),1,1)
    combined$end[x] <- substr(gsub("[^A-Za-z]", "", combined$variant[x]),2,2)
    combined$position[x] <- gsub("[^0-9]", "", combined$variant[x])
    if(combined$start[x] == combined$end[x]){combined$class[x] <- "synonymous"}
  }
}
combined <- combined %>% filter(position != "")

paste("Number of variants that were not scored before but now have scores",nrow(combined %>% filter(is.na(score_orig) & !is.na(score_abundance))))
```

    ## [1] "Number of variants that were not scored before but now have scores 764"

``` r
paste("Number of variants that were originally scored but given new data with the fill-in experiments:",nrow(combined %>% filter(!is.na(score_orig)) %>% filter((!is.na(score9) | !is.na(score10) | !is.na(score11) | !is.na(score12) | !is.na(score13) | !is.na(score14) | !is.na(score15))) %>% filter(count_total >= 4)))
```

    ## [1] "Number of variants that were originally scored but given new data with the fill-in experiments: 3351"

``` r
paste("Number of total PTEN variants currently scored:",round(nrow(subset(combined, !is.na(score_abundance))),2))
```

    ## [1] "Number of total PTEN variants currently scored: 4721"

``` r
paste("Number of synonymous PTEN variants currently scored:",round(nrow(subset(combined, !is.na(score_abundance) & class == "synonymous")),2))
```

    ## [1] "Number of synonymous PTEN variants currently scored: 174"

``` r
paste("Number of nonsense PTEN variants currently scored:",round(nrow(subset(combined, !is.na(score_abundance) & class == "nonsense")),2))
```

    ## [1] "Number of nonsense PTEN variants currently scored: 160"

``` r
paste("Number of missense PTEN variants currently scored:",round(nrow(subset(combined, !is.na(score_abundance) & class == "missense")),2))
```

    ## [1] "Number of missense PTEN variants currently scored: 4387"

``` r
paste("Number of variants that were not scored before but got a score after the second dataset:",round(nrow(subset(combined, is.na(score_orig) & !is.na(score_abundance))),2))
```

    ## [1] "Number of variants that were not scored before but got a score after the second dataset: 764"

``` r
paste("Number of variants that received adjusted scores:",round(nrow(subset(combined, !is.na(score_orig) & score_orig != score_abundance)),2))
```

    ## [1] "Number of variants that received adjusted scores: 3904"

``` r
paste("Number of low abundance PTEN variants intepreted in total:",round(nrow(subset(combined, abundance_class %in% c("low"))),2))
```

    ## [1] "Number of low abundance PTEN variants intepreted in total: 1423"

``` r
paste("Number of WT-like abundance PTEN variants intepreted in total:",round(nrow(subset(combined, abundance_class %in% c("wt-like"))),2))
```

    ## [1] "Number of WT-like abundance PTEN variants intepreted in total: 1738"

``` r
paste("The number of additional low abundance variants identified in the combined dataset:",nrow(subset(combined, abundance_class %in% c("low"))) - nrow(subset(combined, abundance_class_orig %in% c("low"))))
```

    ## [1] "The number of additional low abundance variants identified in the combined dataset: 163"

``` r
paste("The number of additional WT-like abundance variants identified in the combined dataset:",nrow(subset(combined, abundance_class %in% c("wt-like"))) - nrow(subset(combined, abundance_class_orig %in% c("wt-like"))))
```

    ## [1] "The number of additional WT-like abundance variants identified in the combined dataset: 161"

``` r
interpreted_subset <- subset(combined, abundance_class %in% c("low","wt-like"))

paste("Fraction of scored variants in the combined study considered low or WT-like:",round(nrow(subset(combined, abundance_class %in% c("low","wt-like"))) / nrow(subset(combined, abundance_class %in% c("low","wt-like","possibly_low","possibly_wt-like"))),2))
```

    ## [1] "Fraction of scored variants in the combined study considered low or WT-like: 0.67"

``` r
paste("Fraction of scored variants in the original study considered low or WT-like:",round(nrow(subset(combined, abundance_class_orig %in% c("low","wt-like")))/nrow(subset(combined, abundance_class_orig %in% c("low","wt-like","possibly_low","possibly_wt-like"))),2))
```

    ## [1] "Fraction of scored variants in the original study considered low or WT-like: 0.64"

``` r
paste("Number of positions where 18 or more missense variants were scored in the end:", sum(data.frame(table((combined %>% filter(class == "missense", !is.na(score_abundance) & variant != "M1V"))$position))$Freq >= 17))
```

    ## [1] "Number of positions where 18 or more missense variants were scored in the end: 61"

``` r
paste("Number of positions where all missense variants were scored in the end:", sum(data.frame(table((combined %>% filter(class == "missense", !is.na(score_abundance) & variant != "M1V"))$position))$Freq == 19))
```

    ## [1] "Number of positions where all missense variants were scored in the end: 22"

``` r
## Also figuring out how many variants enter each abundance class
abundance_class_summary <- merge(data.frame(table(combined$abundance_class_orig)),data.frame(table(combined$abundance_class)) %>% filter(Var1 != "unknown"), by = "Var1")
colnames(abundance_class_summary) <- c("abundance_class","Original","Composite")
abundance_class_summary_melt <- melt(abundance_class_summary, id = "abundance_class")

Abundance_class_original_composite <- ggplot() + theme(panel.grid.major.x = element_blank()) + labs(x = NULL, y = "Number of variants") +
  scale_fill_manual(values = c("Original" = "blue", "Composite" = "red")) +
  geom_bar(data = abundance_class_summary_melt, aes(x = abundance_class, y = value, fill = variable), stat = "identity", alpha = 0.75, position_dodge(), color = "black")
Abundance_class_original_composite
```

![](PTEN_composite_analysis_files/figure-gfm/Combined%20data-1.png)<!-- -->

``` r
ggsave(file = "Plots/Abundance_class_original_composite.pdf", Abundance_class_original_composite, height = 40, width = 90, units = "mm")
```

``` r
write.table(file = "output_datatables/Composite_abundance_data.tsv", combined, sep = "\t", quote = F, row.names = F)
```

# Updating the ClinVar assessments with the composite abundance dataset

#### Bringing in a more recent PTEN ClinVar dataset

``` r
## Add annotations for Clinvar
clinvar <- read.table(file = "input_datatables/20210415_PTEN_clinvar_missense_nonsense.tsv", header = TRUE, sep = "\t")
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
pten_gnomad <- read.csv(file = "input_datatables/gnomAD_v2.1.1_(non-TOPMed)_ENSG00000171862_2021_04_20_16_18_13.csv", header = T, stringsAsFactors = F)
pten_gnomad <- subset(pten_gnomad, !(VEP.Annotation %in% c("splice_donor_variant","splice_donor")) & VEP.Annotation %in% c("missense_variant","stop_gained"))
pten_gnomad$variant <- substr(pten_gnomad$Protein.Consequence,3,15)
pten_gnomad$position <- gsub("[A-Za-z]","",pten_gnomad$variant)
for(x in 1:nrow(pten_gnomad)){
  pten_gnomad$start[x] <- to_single_notation(substr(gsub("[0-9]","",pten_gnomad$variant[x]),1,3))
  pten_gnomad$end[x] <- to_single_notation(substr(gsub("[0-9]","",pten_gnomad$variant[x]),4,6))
  pten_gnomad$variant[x] <- paste(pten_gnomad$start[x],pten_gnomad$position[x],pten_gnomad$end[x],sep="")
}
colnames(pten_gnomad)[colnames(pten_gnomad) == "Allele.Count"] <- "gnomad_allele_count"
colnames(pten_gnomad)[colnames(pten_gnomad) == "Allele.Number"] <- "gnomad_allele_number"
pten_gnomad_variant <- pten_gnomad %>% group_by(variant) %>% summarize(gnomad_bravo_allele_count = sum(gnomad_allele_count), gnomad_bravo_allele_number = max(gnomad_allele_number), .groups = "drop")

pten_bravo <- read.csv(file = "input_datatables/PTEN_BRAVO_210420_ENSG00000171862.csv", header = T, stringsAsFactors = F)
pten_bravo <- pten_bravo[!grepl("frameshift",pten_bravo$Annotation),]
pten_bravo$type <- ""
for(x in 1:nrow(pten_bravo)){
  pten_bravo$variant[x] <- substr(strsplit(pten_bravo$Consequence[x],";",1)[[1]][1],3,15)
  pten_bravo$position[x] <- gsub("[A-Za-z]","",pten_bravo$variant[x])
  pten_bravo$start[x] <- to_single_notation(substr(gsub("[0-9]","",pten_bravo$variant[x]),1,3))
  pten_bravo$end[x] <- to_single_notation(substr(gsub("[0-9]","",pten_bravo$variant[x]),4,6))
  pten_bravo$variant[x] <- paste(pten_bravo$start[x],pten_bravo$position[x],pten_bravo$end[x],sep="")
  if(pten_bravo$start[x] == pten_bravo$end[x]){pten_bravo$type[x] <- "synonymous"}
}
colnames(pten_bravo)[colnames(pten_bravo) == "Het"] <- "bravo_allele_count"
pten_bravo$bravo_allele_number <- 132345 #TOPMed Freeze 8 on GRCh38
pten_bravo_variant <- pten_bravo %>% group_by(variant) %>% summarize(gnomad_bravo_allele_count = sum(bravo_allele_count), gnomad_bravo_allele_number = max(bravo_allele_number), .groups = "drop")

pten_gnomad_bravo_variant <- rbind(pten_gnomad_variant[,c("variant","gnomad_bravo_allele_count","gnomad_bravo_allele_number")], pten_bravo_variant[,c("variant","gnomad_bravo_allele_count","gnomad_bravo_allele_number")]) %>% group_by(variant) %>% summarize(gnomad_bravo_allele_count = sum(gnomad_bravo_allele_count), gnomad_bravo_allele_number = sum(gnomad_bravo_allele_number), .groups = "drop")

pten_gnomad_bravo_variant$gnomad_bravo_allele_number <- max(pten_gnomad_bravo_variant$gnomad_bravo_allele_number)

combined_clinvar_gnomad_bravo <- merge(combined_clinvar, pten_gnomad_bravo_variant[,c("variant","gnomad_bravo_allele_count","gnomad_bravo_allele_number")], all.x = T)

combined_clinvar_gnomad_bravo$above_gnomad_allele_count_threshold_for_cowdens <- NA

collective_pten_cowdens_allele_frequency <- 1/400000

for(x in 1:nrow(combined_clinvar_gnomad_bravo)){
  if(!is.na(combined_clinvar_gnomad_bravo$gnomad_bravo_allele_count[x])){
    if(combined_clinvar_gnomad_bravo$gnomad_bravo_allele_count[x] > qbinom(0.99, size = combined_clinvar_gnomad_bravo$gnomad_bravo_allele_number[x], collective_pten_cowdens_allele_frequency / 0.95)){
      combined_clinvar_gnomad_bravo$above_gnomad_allele_count_threshold_for_cowdens[x] <- "above threshold"
    if(combined_clinvar_gnomad_bravo$gnomad_bravo_allele_count[x] <= qbinom(0.99, size = combined_clinvar_gnomad_bravo$gnomad_bravo_allele_number[x], collective_pten_cowdens_allele_frequency / 0.95)){
      combined_clinvar_gnomad_bravo$above_gnomad_allele_count_threshold_for_cowdens[x] <- "below threshold"
    }
    }
  }
}

write.csv(file = "output_datatables/combined_clinvar_gnomad_bravo.csv", combined_clinvar_gnomad_bravo, quote = FALSE, row.names = FALSE)
```

## This is where the new biological analyses with the ClinVar and GnomAD data begins

``` r
custom_colorscale <- c("low" = "#3366ff","possibly_low" = "#b3d9ff","possibly_wt-like" = "#ffcccc","wt-like" = "#F8766D","dominant_negative" = "yellow","high" = "brown","unknown" = "grey75")

combined_for_plotting_clinvar <- rbind(
  combined_clinvar_gnomad_bravo %>% filter(snv == 1) %>% mutate(clinvar = "All SNV"),
  combined_clinvar_gnomad_bravo %>% filter(clinvar_pathog == 1) %>% mutate(clinvar = "Pathog"),
  combined_clinvar_gnomad_bravo %>% filter(clinvar_likely_pathog == 1) %>% mutate(clinvar = "Likely pathog"),
  combined_clinvar_gnomad_bravo %>% filter(clinvar_uncertain == 1) %>% mutate(clinvar = "Uncertain"),
  combined_clinvar_gnomad_bravo %>% filter(above_gnomad_allele_count_threshold_for_cowdens == "above threshold") %>% mutate(clinvar = "GnomAD inferred benign")
  )

all_snv_table <- data.frame(table((subset(combined_clinvar_gnomad_bravo, snv == 1))$abundance_class))
colnames(all_snv_table) <- c("abundance_class","count")
all_snv_table$count_interpreted <- all_snv_table$count
all_snv_table[all_snv_table$abundance_class == "unknown","count_interpreted"] <- 0
all_snv_table[all_snv_table$abundance_class == "low","count_interpreted"] / sum(all_snv_table$count_interpreted)
```

    ## [1] 0.2741722

``` r
pathogenic_table <- data.frame(table((subset(combined_clinvar_gnomad_bravo, clinvar_pathog == 1))$abundance_class))
colnames(pathogenic_table) <- c("abundance_class","count")
pathogenic_table$count_interpreted <- pathogenic_table$count
pathogenic_table[pathogenic_table$abundance_class == "unknown","count_interpreted"] <- 0
pathogenic_table[pathogenic_table$abundance_class == "low","count_interpreted"] / sum(pathogenic_table$count_interpreted)
```

    ## [1] 0.7903226

``` r
likelypathog_table <- data.frame(table((subset(combined_clinvar_gnomad_bravo, clinvar_likely_pathog == 1))$abundance_class))
colnames(likelypathog_table) <- c("abundance_class","count")
likelypathog_table$count_interpreted <- likelypathog_table$count
likelypathog_table[likelypathog_table$abundance_class == "unknown","count_interpreted"] <- 0
likelypathog_table[likelypathog_table$abundance_class == "low","count_interpreted"] / sum(likelypathog_table$count_interpreted)
```

    ## [1] 0.6037736

``` r
plp_table <- data.frame(table((subset(combined_clinvar_gnomad_bravo, clinvar_likely_pathog == 1 | clinvar_pathog == 1))$abundance_class))
colnames(plp_table) <- c("abundance_class","count")
plp_table$count_interpreted <- plp_table$count
plp_table[plp_table$abundance_class == "unknown","count_interpreted"] <- 0
plp_table[plp_table$abundance_class == "low","count_interpreted"] / sum(plp_table$count_interpreted)
```

    ## [1] 0.7181818

``` r
combined_for_plotting_clinvar$clinvar <- factor(combined_for_plotting_clinvar$clinvar, levels = c("All SNV","Pathog","Likely pathog","Uncertain","GnomAD inferred benign"))

Clinvar_plots_supplementary <- ggplot() + 
  theme_bw() + theme(legend.position = "top") +
  scale_fill_manual(values = custom_colorscale) + scale_color_manual(values = custom_colorscale) +
  geom_histogram(data = subset(combined_for_plotting_clinvar, class == "missense"), aes(x = score_abundance, fill = abundance_class), binwidth = 0.1, alpha = 0.5, position="stack", color = "black") + 
  facet_grid(rows = vars(clinvar), scale = "free_y")
Clinvar_plots_supplementary
```

    ## Warning: Removed 1135 rows containing non-finite values (stat_bin).

![](PTEN_composite_analysis_files/figure-gfm/Abundance%20score%20histogram-1.png)<!-- -->

``` r
ggsave(file = "plots/Clinvar_plots_supplementary.pdf", Clinvar_plots_supplementary, height = 140, width = 80, units = "mm")
```

    ## Warning: Removed 1135 rows containing non-finite values (stat_bin).

#### Printing out commands that can be used in Pymol (crystal structure 2d5r)

``` r
paste("select substrate, resi 1352","show spheres, substrate","color magenta, substrate", sep = ";")
```

    ## [1] "select substrate, resi 1352;show spheres, substrate;color magenta, substrate"

``` r
paste("select pathog_stable, not name c+n+o and resi", gsub(", ","+",toString(as.character(subset(combined_clinvar, class == "missense" & clinvar_pathog == 1 & snv == 1 & abundance_class == "wt-like")$position))),"; show spheres, pathog_stable; color red, pathog_stable")
```

    ## [1] "select pathog_stable, not name c+n+o and resi 24+93+12+130+14+15+47 ; show spheres, pathog_stable; color red, pathog_stable"

``` r
paste("select likely_pathog_stable, not name c+n+o and resi", gsub(", ","+",toString(as.character(subset(combined_clinvar, class == "missense" & clinvar_likely_pathog == 1 & snv == 1 & abundance_class == "wt-like")$position))),"; show spheres, likely_pathog_stable; color salmon, likely_pathog_stable")
```

    ## [1] "select likely_pathog_stable, not name c+n+o and resi 124+124+24+24+92+90+35+35+14+159+15+15+53 ; show spheres, likely_pathog_stable; color salmon, likely_pathog_stable"

``` r
## Rotate the pymol view
paste("rotate x, -90")
```

    ## [1] "rotate x, -90"

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

abundance_normal_percentile_low <- median((subset(combined_clinvar_gnomad_bravo, class == "synonymous"))$score_total, na.rm = T)
abundance_normal_percentile_high <- quantile((subset(combined_clinvar_gnomad_bravo, class == "synonymous"))$score_total, 0.95, na.rm = T) 

abundance_low_percentile <- median((subset(combined_clinvar_gnomad_bravo, class == "nonsense"))$score_total, na.rm = T) #quantile(normal_dist_fit_low$prob, 0.90)

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

library(ggdendro)
#convert cluster object to use with ggplot
dendr <- dendro_data(hclust(dist(pten_double2)), type="rectangle") 

dendrogram_plot <- ggplot() + 
  geom_segment(data=segment(dendr), aes(x=x, y=y, xend=xend, yend=yend)) + 
  geom_text(data=NULL, aes(x=dendr$label$x, y=dendr$label$y, label=dendr$label$label, hjust=0, angle = 90), size=3) +
  #geom_text(data=label(dendr), aes(x=x, y=y, label=label, hjust=0), size=3) +
  scale_y_reverse(expand=c(0.2, 0)) + 
  theme(axis.line.y=element_blank(),
        axis.ticks.y=element_blank(),
        axis.text.y=element_blank(),
        axis.title.y=element_blank(),
        panel.background=element_rect(fill="white"),
        panel.grid=element_blank())

ggsave(file = "plots/dendrogram_plot.pdf", dendrogram_plot, height = 80, width = 178*2, units = "mm")
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
  scale_y_continuous(expand = c(0,0.1), breaks = c(0,5,10)) +
  geom_hline(yintercept = 0, size = 1.5) +
  geom_histogram(data = subset(gini_frame, gini <= 0.121), aes(x = gini), binwidth = 0.02, color = "black", fill = "blue", alpha = 0.8) +
  geom_histogram(data = subset(gini_frame, gini > 0.121 & gini <= 0.24), aes(x = gini), binwidth = 0.02, color = "black", fill = "thistle2", alpha =  0.8) +
  geom_histogram(data = subset(gini_frame, gini > 0.24), aes(x = gini), binwidth = 0.02, color = "black", fill = "red", alpha =  0.8)
Gini_coefficient_plot
```

![](PTEN_composite_analysis_files/figure-gfm/Gini%20coefficient-1.png)<!-- -->

``` r
ggsave(file = "plots/Gini_coefficient_plot.pdf", Gini_coefficient_plot, height = 25, width = 35, units = "mm")

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

``` r
combined_for_heatmap <- combined

combined_for_heatmap$position <- as.numeric(combined_for_heatmap$position)
combined_for_heatmap$end <- factor(combined_for_heatmap$end, levels = c("G","S","T","C","A","M","W","Y","F","L","I","V","D","E","N","Q","H","K","R","P","X"))

combined_for_heatmap[!is.na(combined_for_heatmap$score_orig) & combined_for_heatmap$score_orig < pten_lower_threshold,"score_orig"] <- pten_lower_threshold
combined_for_heatmap[!is.na(combined_for_heatmap$score_abundance) & combined_for_heatmap$score_abundance < pten_lower_threshold,"score_abundance"] <- pten_lower_threshold

PTEN_full_heatmap <- ggplot() + theme(panel.background = element_rect("grey80"), panel.grid.major = element_blank()) +
  geom_tile(data = combined_for_heatmap, aes(x = position, y = end, fill = score_orig), width = 1) +
  geom_tile(data = combined_for_heatmap, aes(x = position, y = end, fill = score_abundance), height = 0.6, width = 0.4) +
  scale_x_continuous(expand = c(0,0)) +
  scale_fill_gradientn(colours = c("blue","white","red"), values = rescale(c(pten_lower_threshold,1,2)), limits=c(pten_lower_threshold,2))
ggsave(fil = "Plots/PTEN_full_heatmap.pdf", PTEN_full_heatmap, height = 3, width = 15)
PTEN_full_heatmap
```

![](PTEN_composite_analysis_files/figure-gfm/Make%20a%20complete%20sequence%20function%20map%20showing%20new%20and%20old%20data-1.png)<!-- -->

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

    ## [1] "Number of variants with abundance scores: 4388"

``` r
count_activity_scores <- nrow(subset(combined_abund_act, !is.na(score_activity) & class == "missense" & high_conf == T))
paste("Number of variants with activity scores:", count_activity_scores)
```

    ## [1] "Number of variants with activity scores: 6562"

#### Making a comparison of abundance and functional data

``` r
complete_abund_act <- subset(combined_abund_act, !is.na(score_abundance) & !(is.na(score_activity)))
complete_abund_act$abund_act_class <- "NA"
paste("Number of missense variants with abundance and activity scores:", nrow(complete_abund_act %>% filter(class == "missense")))
```

    ## [1] "Number of missense variants with abundance and activity scores: 4178"

``` r
for(x in 1:nrow(complete_abund_act)){
  if(!(is.na(complete_abund_act$score_activity[x])) & !(is.na(complete_abund_act$score_abundance[x]))){
    if((complete_abund_act$abundance_class[x] == "low") & (complete_abund_act$score_activity[x] > activity_syn_5th)){complete_abund_act$abund_act_class[x] <- "2_loss_of_abundance_only"}
    if((complete_abund_act$abundance_class[x] == "wt-like") & (complete_abund_act$score_activity[x] < activity_nonsense_5th)){complete_abund_act$abund_act_class[x] <- "4_loss_of_activity_only"}
    if((complete_abund_act$abundance_class[x] == "low") & (complete_abund_act$score_activity[x] < activity_nonsense_5th)){complete_abund_act$abund_act_class[x] <- "3_loss_of_both"}
    if((complete_abund_act$abundance_class[x] == "wt-like") & (complete_abund_act$score_activity[x] > activity_syn_5th)){complete_abund_act$abund_act_class[x] <- "1_wt_like"}
  }
}

complete_abund_act$abund_act_class <- factor(complete_abund_act$abund_act_class, levels = c("2_loss_of_abundance_only","4_loss_of_activity_only","3_loss_of_both","1_wt_like","NA"))

custom_colorscale2 <- c("2_loss_of_abundance_only" = "turquoise","4_loss_of_activity_only" = "orange","3_loss_of_both" = "purple","1_wt_like" = "dark green", "NA" = "grey75")
complete_abund_act_missense <- subset(complete_abund_act, class == "missense" & !is.na(score_abundance) & !(is.na(score_activity)))
```

``` r
complete_table <- data.frame(table(complete_abund_act_missense$position))
complete_table <- complete_table[order(complete_table$Freq, decreasing = T),]

loss_of_abundance_table <- data.frame(table(subset(complete_abund_act_missense, abund_act_class == "2_loss_of_abundance_only")$position))
loss_of_abundance_table <- loss_of_abundance_table[order(loss_of_abundance_table$Freq, decreasing = T),]

loss_of_activity_table <- data.frame(table(subset(complete_abund_act_missense, abund_act_class == "4_loss_of_activity_only")$position))
loss_of_activity_table <- loss_of_activity_table[order(loss_of_activity_table$Freq, decreasing = T),]

complete_table <- merge(complete_table, loss_of_abundance_table, by = "Var1", all.x = T)
complete_table <- merge(complete_table, loss_of_activity_table, by = "Var1", all.x = T)
colnames(complete_table) <- c("position","complete","loss_of_abundance","loss_of_activity")
complete_table[is.na(complete_table)] <- 0

loss_of_both_table <- data.frame(table(subset(complete_abund_act_missense, abund_act_class == "3_loss_of_both")$position))
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

    ## [1] "select low_diff, resi 169+172+188+246+247+258+270+274+278+280+322+331+337+348+388+58+66 and not name c+n+o"

``` r
paste("select high_diff, resi",gsub(", ","+",toString(high_abund_act_diff$position)), "and not name c+n+o")
```

    ## [1] "select high_diff, resi 123+125+130+15+159+333+401+47+92 and not name c+n+o"

``` r
paste("select low, resi",gsub(", ","+",toString(low_total$position)), "and not name c+n+o")
```

    ## [1] "select low, resi 101+104+105+107+108+111+119+120+122+131+136+137+140+148+166+170+175+177+195+217+241+249+25+252+253+255+27+271+275+277+28+325+326+346+35+53+56+57+61+67+68+95 and not name c+n+o"

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
  geom_vline(xintercept = quantile(subset(complete_abund_act_missense, abundance_class == "low")$score_abundance,0.99), linetype = 2, color = "blue", alpha = 0.5) +
  geom_text(aes(x = -0.2, y = 1.6, label = paste("n=",nrow(subset(complete_abund_act_missense, abund_act_class == "2_loss_of_abundance_only")))), color = "turquoise", hjust = 0) +
  geom_text(aes(x = -0.2, y = 1.45, label = paste("n=",nrow(subset(complete_abund_act_missense, abund_act_class == "NA" & score_activity > activity_syn_5th & score_abundance < quantile(subset(complete_abund_act_missense, abundance_class == "low")$score_abundance,0.99) )))), color = "grey50", hjust = 0) +
  geom_text(aes(x = -0.2, y = -0.25, label = paste("n=",nrow(subset(complete_abund_act_missense, abund_act_class == "3_loss_of_both")))), color = "purple", hjust = 0) +
  geom_text(aes(x = -0.2, y = -0.4, label = paste("n=",nrow(subset(complete_abund_act_missense, abund_act_class == "NA" & score_activity < activity_nonsense_5th & score_abundance < quantile(subset(complete_abund_act_missense, abundance_class == "low")$score_abundance,0.99) )))), color = "grey50", hjust = 0) +
  geom_text(aes(x = 1.4, y = 1.6, label = paste("n=",nrow(subset(complete_abund_act_missense, abund_act_class == "1_wt_like")))), color = "dark green", hjust = 1) +
  geom_text(aes(x = 1.4, y = 1.45, label = paste("n=",nrow(subset(complete_abund_act_missense, abund_act_class == "NA" & score_activity > activity_syn_5th & score_abundance < quantile(subset(complete_abund_act_missense, abundance_class == "wt-like")$score_abundance,0.01, na.rm = T) )))), color = "grey50", hjust = 1) +
  geom_text(aes(x = 1.4, y = -0.25, label = paste("n=",nrow(subset(complete_abund_act_missense, abund_act_class == "4_loss_of_activity_only")))), color = "orange", hjust = 1) +
  geom_text(aes(x = 1.4, y = -0.4, label = paste("n=",nrow(subset(complete_abund_act_missense, abund_act_class == "NA" & score_activity < activity_nonsense_5th & score_abundance < quantile(subset(complete_abund_act_missense, abundance_class == "wt-like")$score_abundance,0.01, na.rm = T) )))), color = "grey50", hjust = 1) +
  geom_text(aes(x = 0.7, y = 1.45, label = paste("n=",nrow(subset(complete_abund_act_missense, abund_act_class == "NA" & score_activity > activity_syn_5th & score_abundance < quantile(subset(complete_abund_act_missense, abundance_class == "wt-like")$score_abundance,0.01, na.rm = T) & score_abundance > quantile(subset(complete_abund_act_missense, abundance_class == "low")$score_abundance,0.99) )))), color = "grey50", hjust = 0.5) +
  geom_text(aes(x = 0.7, y = -0.4, label = paste("n=",nrow(subset(complete_abund_act_missense, abund_act_class == "NA" & score_activity < activity_nonsense_5th & score_abundance < quantile(subset(complete_abund_act_missense, abundance_class == "wt-like")$score_abundance,0.01, na.rm = T) & score_abundance > quantile(subset(complete_abund_act_missense, abundance_class == "low")$score_abundance,0.99) )))), color = "grey50", hjust = 0.5) +
  geom_text(aes(x = -0.2, y = 0.6, label = paste("n=",nrow(subset(complete_abund_act_missense, abund_act_class == "NA" & score_activity > activity_nonsense_5th & score_activity < activity_syn_5th & score_abundance < quantile(subset(complete_abund_act_missense, abundance_class == "low")$score_abundance,0.99) )))), color = "grey50", hjust = 0) +
  geom_text(aes(x = 1.4, y = 0.6, label = paste("n=",nrow(subset(complete_abund_act_missense, abund_act_class == "NA" & score_activity > activity_nonsense_5th & score_activity > activity_syn_5th & score_abundance > quantile(subset(complete_abund_act_missense, abundance_class == "wt-like")$score_abundance,0.01, na.rm = T) )))), color = "grey50", hjust = 1)
quadrant_plot
```

![](PTEN_composite_analysis_files/figure-gfm/How%20about%20literally%20just%20subtracting%20abundance%20by%20activity-1.png)<!-- -->

``` r
ggsave(file = "plots/quadrant_plot.pdf", quadrant_plot, height = 80, width = 80, units = "mm")

paste("Number of confidently assessed PTEN variants:",nrow(subset(complete_abund_act_missense, abund_act_class != "NA")))
```

    ## [1] "Number of confidently assessed PTEN variants: 2377"

``` r
paste("Fraction of confidently assessed PTEN variants that were WT-like for both:",nrow(subset(complete_abund_act_missense, abund_act_class == "1_wt_like"))/nrow(subset(complete_abund_act_missense, abund_act_class != "NA")))
```

    ## [1] "Fraction of confidently assessed PTEN variants that were WT-like for both: 0.511148506520825"

``` r
paste("Fraction of confidently assessed PTEN variants that were WT-like for both:",nrow(subset(complete_abund_act_missense, abund_act_class == "3_loss_of_both"))/nrow(subset(complete_abund_act_missense, abund_act_class != "NA")))
```

    ## [1] "Fraction of confidently assessed PTEN variants that were WT-like for both: 0.211190576356752"

``` r
paste("Fraction of confidently assessed PTEN variants that were WT-like for both:",nrow(subset(complete_abund_act_missense, abund_act_class == "2_loss_of_abundance_only"))/nrow(subset(complete_abund_act_missense, abund_act_class != "NA")))
```

    ## [1] "Fraction of confidently assessed PTEN variants that were WT-like for both: 0.215397559949516"

``` r
paste("Fraction of confidently assessed PTEN variants that were WT-like for both:",nrow(subset(complete_abund_act_missense, abund_act_class == "4_loss_of_activity_only"))/nrow(subset(complete_abund_act_missense, abund_act_class != "NA")))
```

    ## [1] "Fraction of confidently assessed PTEN variants that were WT-like for both: 0.062263357172907"

``` r
quadrant_plot <- ggplot() + 
  theme_classic() +
  theme(legend.position = "none", panel.grid.major = element_line("grey95")) +
  xlab("Abundance score") + ylab("Activity score") +
  scale_x_continuous(breaks = c(0,1)) + 
  scale_y_continuous(breaks = c(0,1)) +
  scale_color_manual(values = custom_colorscale2) +
  geom_point(data = complete_abund_act_missense, aes(x = score_abundance, y = score_activity, color = abund_act_class), alpha = 0.2)

n <- 1000
x <- mvrnorm(n, mu=c(.5,2.5), Sigma=matrix(c(1,.6,.6,1), ncol=2))
df = data.frame(x); colnames(df) = c("x","y")
commonTheme = list(labs(color="Density",fill="Density",
                        x="Activity score",
                        y="Abundance score"),
                   theme_bw(),
                   theme(legend.position = "none",
                         legend.justification=c(0,1)))
PTEN_density_plot <- ggplot() +  theme(legend.position = "none") +
  labs(x = "Abundance score", y = "Activity score") + 
  geom_hline(yintercept = c(0,1), color = "grey75", linetype = 2) + geom_vline(xintercept = c(0,1), color = "grey75", linetype = 2) +
  geom_point(data = complete_abund_act_missense, aes(x = score_abundance, y = score_activity), alpha = 0.02) +
  geom_density2d(data = complete_abund_act_missense, aes(x = score_abundance, y = score_activity, colour=..level..), adjust = 0.8, size = 0.75) + 
  geom_segment(aes(x = 0.35, y = 0.9, xend = 0.95, yend = 1), size = 10, alpha = 0.15, color = "blue", lineend = "round") +
  geom_segment(aes(x = 0.35, y = 0.9, xend = 0.25, yend = 0.1), size = 10, alpha = 0.15, color = "blue", lineend = "round") +
  scale_colour_gradient(low="green",high="red") + scale_y_continuous(limits = c(-0.2,1.4), expand = c(0,0)) + scale_x_continuous(limits = c(0,1.4), expand = c(0,0))
PTEN_density_plot
```

    ## Warning: Removed 43 rows containing non-finite values (stat_density2d).

    ## Warning: Removed 43 rows containing missing values (geom_point).

![](PTEN_composite_analysis_files/figure-gfm/Final%20plot%20to%20show%20the%20relationship%20between%20the%20PTEN%20activity%20and%20abundance%20assays-1.png)<!-- -->

``` r
ggsave(file = "plots/PTEN_density_plot.png", PTEN_density_plot, height = 2.5, width = 3)
```

    ## Warning: Removed 43 rows containing non-finite values (stat_density2d).

    ## Warning: Removed 43 rows containing missing values (geom_point).

``` r
sfari <- read.delim(file = "input_datatables/Sfari_20210415.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% filter(variant_type %in% c("missense_variant","stop_gained")) %>% filter(residue_change != "-")

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

asd_summary <- data.frame(table(sfari$variant))
colnames(asd_summary) <- c("variant","asd")

## Now bring in the Mighell et al data

cc_cohort1 <- read.csv(file = "input_datatables/Mighell_et_al_table_S3.csv", header = T, stringsAsFactors = F)
cc_cohort2 <- read.csv(file = "input_datatables/Mighell_et_al_table_S4.csv", header = T, stringsAsFactors = F)

cc_cohort1a <- cc_cohort1[,c("Subject_ID","AA_one_letter","Phenotype_Class")]
colnames(cc_cohort1a) <- c("Subject_ID","variant","Phenotype_Class")
cc_cohort2a <- cc_cohort2[,c("Universal_ID","Prot_change","Phenotype_Class")]
colnames(cc_cohort2a) <- c("Subject_ID","variant","Phenotype_Class")

cc_cohort2a$variant <- gsub("[*]", "X", cc_cohort2a$variant)
cc_cohort <- rbind(cc_cohort1a[,c("Subject_ID","variant","Phenotype_Class")],cc_cohort2a[,c("Subject_ID","variant","Phenotype_Class")]) %>% filter(!is.na(Phenotype_Class))

cc_cohort$asd_dd <- 0
cc_cohort$phts <- 0

for(x in 1:nrow(cc_cohort)){
  if(grepl(cc_cohort$Phenotype_Class[x],"ASD/DD")){cc_cohort$asd_dd[x] <- 1}
  if(grepl(cc_cohort$Phenotype_Class[x],"PHTS")){cc_cohort$phts[x] <- 1}
}

cc_cohort_summary <- cc_cohort %>% group_by(variant) %>% summarize(asd_dd = mean(asd_dd), phts = mean(phts))
cc_cohort_summary[cc_cohort_summary$asd_dd != 0,"asd_dd"] <- as.integer(1)
cc_cohort_summary[cc_cohort_summary$phts != 0,"phts"] <- as.integer(1)


## Merge the new data into the old datatable
complete_abund_act_missense2 <- merge(complete_abund_act_missense, asd_summary, by = "variant", all.x = T)
complete_abund_act_missense2 <- merge(complete_abund_act_missense2, cc_cohort_summary, by = "variant", all.x = T)

complete_abund_act_missense2[is.na(complete_abund_act_missense2$asd),"asd"] <- 0
complete_abund_act_missense2[is.na(complete_abund_act_missense2$asd_dd),"asd_dd"] <- 0
complete_abund_act_missense2[is.na(complete_abund_act_missense2$phts),"phts"] <- 0

complete_abund_act_missense2 <- merge(complete_abund_act_missense2, (combined_clinvar_gnomad_bravo %>% filter(!is.na(gnomad_bravo_allele_count)))[,c("variant","gnomad_bravo_allele_count")], by = "variant", all.x = T)
complete_abund_act_missense2[is.na(complete_abund_act_missense2$gnomad_bravo_allele_count),"gnomad_bravo_allele_count"] <- 0
complete_abund_act_missense2[complete_abund_act_missense2$gnomad_bravo_allele_count != 0,"gnomad"] <- 1
complete_abund_act_missense2[is.na(complete_abund_act_missense2$gnomad),"gnomad"] <- 0

clinvar_abundance_activity_aggregate <- rbind(
  (complete_abund_act_missense2 %>% filter(snv == 1) %>% mutate(grouping = "All_SNV"))[,c("variant","grouping","score_abundance","abund_act_class")],
  (complete_abund_act_missense2 %>% filter((clinvar_pathog == 1 | clinvar_likely_pathog == 1 | phts == 1) & asd == 0 & asd_dd == 0 & snv == 1) %>% mutate(grouping = "P_LP_only"))[,c("variant","grouping","score_abundance","abund_act_class")],
  (complete_abund_act_missense2 %>% filter(clinvar_uncertain == 1 & snv == 1) %>% mutate(grouping = "VUS"))[,c("variant","grouping","score_abundance","abund_act_class")],
  (complete_abund_act_missense2 %>% filter(snv == 1 & (asd >= 1 | asd_dd >= 1) & clinvar_pathog == 0 & clinvar_likely_pathog == 0 & phts == 0) %>% mutate(grouping = "ASD_only"))[,c("variant","grouping","score_abundance","abund_act_class")],
  (complete_abund_act_missense2 %>% filter((clinvar_pathog == 1 | clinvar_likely_pathog == 1 | phts == 1) & snv == 1 & (asd >= 1 | asd_dd >= 1)) %>% mutate(grouping = "P_LP_and_ASD"))[,c("variant","grouping","score_abundance","abund_act_class")],
  (complete_abund_act_missense2 %>% filter(snv == 1 & gnomad == 1) %>% mutate(grouping = "GnomAD"))[,c("variant","grouping","score_abundance","abund_act_class")])

clinvar_abundance_activity_aggregate$grouping <- factor(clinvar_abundance_activity_aggregate$grouping, levels = c("All_SNV","P_LP_only","VUS","ASD_only","P_LP_and_ASD","GnomAD"))
clinvar_abundance_activity_aggregate2 <- subset(clinvar_abundance_activity_aggregate, abund_act_class != "NA")

clinvar_abundance_activity_aggregate2_summary <- data.frame(table(subset(clinvar_abundance_activity_aggregate2, grouping == "All_SNV")$abund_act_class))
clinvar_abundance_activity_aggregate2_summary <- merge(clinvar_abundance_activity_aggregate2_summary, data.frame(table(subset(clinvar_abundance_activity_aggregate2, grouping == "P_LP_only")$abund_act_class)), by = "Var1")
clinvar_abundance_activity_aggregate2_summary <- merge(clinvar_abundance_activity_aggregate2_summary, data.frame(table(subset(clinvar_abundance_activity_aggregate2, grouping == "VUS")$abund_act_class)), by = "Var1")
clinvar_abundance_activity_aggregate2_summary <- merge(clinvar_abundance_activity_aggregate2_summary, data.frame(table(subset(clinvar_abundance_activity_aggregate2, grouping == "ASD_only")$abund_act_class)), by = "Var1")
```

    ## Warning in merge.data.frame(clinvar_abundance_activity_aggregate2_summary, :
    ## column names 'Freq.x', 'Freq.y' are duplicated in the result

``` r
clinvar_abundance_activity_aggregate2_summary <- merge(clinvar_abundance_activity_aggregate2_summary, data.frame(table(subset(clinvar_abundance_activity_aggregate2, grouping == "P_LP_and_ASD")$abund_act_class)), by = "Var1")
```

    ## Warning in merge.data.frame(clinvar_abundance_activity_aggregate2_summary, :
    ## column names 'Freq.x', 'Freq.y' are duplicated in the result

``` r
clinvar_abundance_activity_aggregate2_summary <- merge(clinvar_abundance_activity_aggregate2_summary, data.frame(table(subset(clinvar_abundance_activity_aggregate2, grouping == "GnomAD")$abund_act_class)), by = "Var1")
```

    ## Warning in merge.data.frame(clinvar_abundance_activity_aggregate2_summary, :
    ## column names 'Freq.x', 'Freq.y', 'Freq.x', 'Freq.y' are duplicated in the result

``` r
colnames(clinvar_abundance_activity_aggregate2_summary) <- c("abund_act_class","All_SNV","P_LP_only","VUS","ASD_only","P_LP_and_ASD","gnomad")

clinvar_abundance_activity_aggregate2_summary <- clinvar_abundance_activity_aggregate2_summary %>% filter(abund_act_class != "NA") %>% mutate(freq_all_snv = All_SNV / sum(All_SNV), freq_P_LP_only = P_LP_only / sum(P_LP_only), freq_VUS = VUS / sum(VUS), freq_ASD_only = ASD_only / sum(ASD_only), freq_P_LP_and_ASD = P_LP_and_ASD / sum(P_LP_and_ASD), freq_gnomad = gnomad / sum(gnomad))

clinvar_abundance_activity_aggregate2_summary_melt <- melt(clinvar_abundance_activity_aggregate2_summary[,c("abund_act_class","freq_all_snv","freq_P_LP_only","freq_VUS","freq_ASD_only","freq_P_LP_and_ASD","freq_gnomad")], id = "abund_act_class")
clinvar_abundance_activity_aggregate2_summary_melt$abund_act_class <- factor(clinvar_abundance_activity_aggregate2_summary_melt$abund_act_class, levels = c("3_loss_of_both","4_loss_of_activity_only","2_loss_of_abundance_only","1_wt_like"))

custom_colorscale3 <- c("3_loss_of_both" = "purple","4_loss_of_activity_only" = "orange","2_loss_of_abundance_only" = "turquoise","1_wt_like" = "dark green")

clinvar_abundance_activity_aggregate2_summary_melt$variable <- as.character(clinvar_abundance_activity_aggregate2_summary_melt$variable)

#clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_all_snv","variable"] <- "All SNV"
#clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_P_LP_only","variable"] <- "P/LP_only"
#clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_VUS","variable"] <- "VUS"
#clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_ASD_only","variable"] <- "ASD_only"
#clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_P_LP_and_ASD","variable"] <- "P/LP_and_ASD"
#clinvar_abundance_activity_aggregate2_summary_melt$variable <- factor(clinvar_abundance_activity_aggregate2_summary_melt$variable, levels = c("All SNV","P/LP_only","P/LP_and_ASD","ASD_only","VUS"))

clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_all_snv","variable"] <- paste("(1) All SNV\nn=",sum(clinvar_abundance_activity_aggregate2_summary$All_SNV))
clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_P_LP_only","variable"] <- paste("(2) P/LP only\nn=",sum(clinvar_abundance_activity_aggregate2_summary$P_LP_only))
clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_P_LP_and_ASD","variable"] <- paste("(3) P/LP and ASD\nn=",sum(clinvar_abundance_activity_aggregate2_summary$P_LP_and_ASD))
clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_ASD_only","variable"] <- paste("(4) ASD only\nn=",sum(clinvar_abundance_activity_aggregate2_summary$ASD_only))
clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_VUS","variable"] <- paste("(5) VUS\nn=",sum(clinvar_abundance_activity_aggregate2_summary$VUS))
clinvar_abundance_activity_aggregate2_summary_melt[clinvar_abundance_activity_aggregate2_summary_melt$variable == "freq_gnomad","variable"] <- paste("(6) GnomAD\nn=",sum(clinvar_abundance_activity_aggregate2_summary$gnomad))

Clinvar_abundance_activity_barplots <- ggplot() + 
  theme(panel.grid.major.x = element_blank(), axis.text.x = element_text(angle = -90, hjust = 0.5, vjust = 0.5), legend.position = "none") +
  xlab(NULL) + ylab("Fraction of variants") +
  scale_fill_manual(values = custom_colorscale3) +
  geom_bar(data = clinvar_abundance_activity_aggregate2_summary_melt, aes(x = variable, y = value, fill = abund_act_class), stat = "identity", alpha = 0.6, color = "black")
Clinvar_abundance_activity_barplots
```

![](PTEN_composite_analysis_files/figure-gfm/Look%20at%20PHTS%20variants%20in%20ClinVar%20and%20autism-associated%20variants%20in%20sfari-1.png)<!-- -->

``` r
ggsave(file = "plots/Clinvar_abundance_activity_barplots.pdf", Clinvar_abundance_activity_barplots, height = 70, width = 80, units = "mm")

#### Noting how many Pathog or Likely Pathog variants are in one of the three loss-of-function categories
paste("The number of Pathog or Likely Pathog in the dataset:",nrow(complete_abund_act_missense2 %>% filter((clinvar_pathog == 1 | clinvar_likely_pathog == 1) & (abund_act_class != "NA"))))
```

    ## [1] "The number of Pathog or Likely Pathog in the dataset: 44"

``` r
#### Noting how many VUS are in one of the three loss-of-function categories
paste("The number of VUS in the dataset:",nrow(complete_abund_act_missense2 %>% filter(clinvar_uncertain != 0 & abund_act_class != "NA")))
```

    ## [1] "The number of VUS in the dataset: 154"

``` r
paste("The number of VUS in the dataset that are low activity or low abundance:",nrow(complete_abund_act_missense2 %>% filter(clinvar_uncertain != 0 & (abundance_class == "low" | score_activity < activity_nonsense_5th) & (abund_act_class != "NA"))))
```

    ## [1] "The number of VUS in the dataset that are low activity or low abundance: 59"

``` r
clinvar_abundance_activity_aggregate2_summary_melt$all_snv_norm <- 0

for(x in 1:nrow(clinvar_abundance_activity_aggregate2_summary_melt)){
  all_snv_set <- clinvar_abundance_activity_aggregate2_summary_melt[seq(1,4),]
  temp_sample_abund_act_class <- clinvar_abundance_activity_aggregate2_summary_melt$abund_act_class[x]
  clinvar_abundance_activity_aggregate2_summary_melt$all_snv_norm[x] <- clinvar_abundance_activity_aggregate2_summary_melt$value[x] / all_snv_set[all_snv_set$abund_act_class == temp_sample_abund_act_class,"value"]
}

Clinvar_abundance_activity_ratios <- ggplot() + theme_bw() + theme(panel.grid.minor = element_blank(), legend.position = "none", axis.text.x = element_text(angle = -90, hjust = 0.5, vjust = 0.5), panel.grid.major.x = element_blank()) + 
  labs(x = NULL, y = "Fraction of All SNV frequency") +
  scale_color_manual(values = custom_colorscale3) +
  scale_y_log10(breaks = c(0.16,0.25,0.5,1,2,4,6)) +
  geom_hline(yintercept = 1, linetype = 2) +
  geom_point(data = clinvar_abundance_activity_aggregate2_summary_melt, aes(x = variable, y = all_snv_norm, color = abund_act_class), position=position_dodge(width=0.6), alpha = 1)
Clinvar_abundance_activity_ratios
```

![](PTEN_composite_analysis_files/figure-gfm/Look%20at%20PHTS%20variants%20in%20ClinVar%20and%20autism-associated%20variants%20in%20sfari-2.png)<!-- -->

``` r
ggsave(file = "plots/Clinvar_abundance_activity_ratios.pdf", Clinvar_abundance_activity_ratios, height = 80, width = 80, units = "mm")
```

## Mighell et al recently imputed some of the missing scores in the initial abundance dataset. See how their imputated values correlated with the actual values we got once we performed the fill-in experiment.

``` r
mighell <- read.csv(file = "input_datatables/Mighell_imputed_abundance.csv")
colnames(mighell)[1] <- "variant"

mighell_imputed <- mighell %>% filter(abundance_score_type == "Imputed")

combined_only_second_library <- combined %>% filter(is.na(score_orig) & !is.na(score_abundance))
combined_only_second_library2 <- merge(combined_only_second_library, mighell_imputed[,c("variant","abundance_score")], by = "variant")

lm_imputed<- lm(combined_only_second_library2$abundance_score ~ combined_only_second_library2$score_abundance)
paste("For a linear model fit to the overlapping data, the slope was",round(lm_imputed$coefficients[2],2),"and the intercept was",round(lm_imputed$coefficients[1],2))
```

    ## [1] "For a linear model fit to the overlapping data, the slope was 0.53 and the intercept was 0.35"

``` r
paste("The Pearson's r^2 for the scored and imputed data is:", round(cor(combined_only_second_library2$score_abundance, combined_only_second_library2$abundance_score, method = "pearson")^2,2))
```

    ## [1] "The Pearson's r^2 for the scored and imputed data is: 0.54"

``` r
real_vs_imputed_plot <- ggplot() + 
  theme_bw() + 
  labs(x = "Abundance score from fillin library", y = "Imputed score by Mighell 2020") +
  scale_x_continuous(limits = c(0,1.2)) + scale_y_continuous(limits = c(0.2,1.1)) +
  geom_abline(slope = 1, intercept = 0, alpha = 0.2, size = 10) +
  geom_abline(slope = lm_imputed$coefficients[2], intercept = lm_imputed$coefficients[1], alpha = 0.2, size = 10, color = "blue") +
  geom_point(data = combined_only_second_library2, aes(x = score_abundance, y = abundance_score), alpha = 0.2) +
  geom_text(aes(x = 0, y = 1, label = paste("n=",nrow(combined_only_second_library2))), hjust = 0) +
  geom_point(data = combined_only_second_library2 %>% filter(position == 173), aes(x = score_abundance, y = abundance_score), alpha = 0.5, color = "red") +
  geom_text(data = NULL, aes(x = 0.25, y = 0.65), label = "R173", color = "red") + 
  geom_point(data = combined_only_second_library2 %>% filter(position %in% c(103,248)), aes(x = score_abundance, y = abundance_score), alpha = 0.5, color = "blue") +
  geom_text(data = NULL, aes(x = 0.95, y = 0.45), label = "P103, P248", color = "blue") + 
  geom_point(data = combined_only_second_library2 %>% filter(position == 180), aes(x = score_abundance, y = abundance_score), alpha = 0.5, color = "orange") +
  geom_text(data = NULL, aes(x = 0.6, y = 0.8), label = "Y180", color = "orange") +
  geom_point(data = combined_only_second_library2 %>% filter(position == 165), aes(x = score_abundance, y = abundance_score), alpha = 0.5, color = "purple") +
  geom_text(data = NULL, aes(x = 0.75, y = 0.35), label = "G165", color = "purple") +
  geom_point(data = combined_only_second_library2 %>% filter(position == 278), aes(x = score_abundance, y = abundance_score), alpha = 0.5, color = "dark green") +
  geom_text(data = NULL, aes(x = 0.65, y = 0.25), label = "F278", color = "dark green") +
  geom_point(data = combined_only_second_library2 %>% filter(position == 251), aes(x = score_abundance, y = abundance_score), alpha = 0.5, color = "magenta") +
  geom_text(data = NULL, aes(x = 0.2, y = 0.35), label = "G251", color = "magenta") +
  geom_point(data = combined_only_second_library2 %>% filter(position == 182), aes(x = score_abundance, y = abundance_score), alpha = 1, color = "cyan") +
  geom_text(data = NULL, aes(x = 0.6, y = 0.5), label = "L182", color = "darkcyan") +
  geom_point(data = combined_only_second_library2 %>% filter(position == 268), aes(x = score_abundance, y = abundance_score), alpha = 1, color = "green") +
  geom_text(data = NULL, aes(x = 0.6, y = 0.65), label = "D268", color = "green4")
real_vs_imputed_plot
```

    ## Warning: Removed 15 rows containing missing values (geom_point).

    ## Warning: Removed 1 rows containing missing values (geom_point).

![](PTEN_composite_analysis_files/figure-gfm/Compare%20Mighell%202020%20imputed%20data-1.png)<!-- -->

``` r
ggsave(file = "plots/Abundance_real_vs_imputed_plot.pdf", real_vs_imputed_plot, height = 50*2, width = 80*2, units = "mm")
```

    ## Warning: Removed 15 rows containing missing values (geom_point).

    ## Warning: Removed 1 rows containing missing values (geom_point).

``` r
## Are there particular positions that were guessed worse?

combined_only_second_library2$difference <- abs(combined_only_second_library2$score_abundance - combined_only_second_library2$abundance_score)

ggplot() + geom_density(data = combined_only_second_library2, aes(x = difference))
```

![](PTEN_composite_analysis_files/figure-gfm/Compare%20Mighell%202020%20imputed%20data-2.png)<!-- -->

``` r
combined_only_second_library3 <- combined_only_second_library2 %>% mutate(count = 1) %>% group_by(position) %>% summarize(mean_difference = mean(difference), total_variants = sum(count))
```

``` r
cbioportal_raw <- read.delim(file = "input_datatables/All_cBioportal_nonredundant_210420.tsv", sep = "\t", header = T, stringsAsFactors = F)
cbioportal_standard <- read.delim(file = "input_datatables/All_cBioportal_nonredundant_210420.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(variant = gsub("[*]","X",Protein.Change)) %>% group_by(Study, Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant), .groups = "drop") %>% mutate(length = nchar(variant)) %>% filter(length <= 5) #%>% filter(!(Sample.ID %in% c("P-0000422-T02-IM3","P-0000657-T02-IM5","P-0001442-T02-IM5","P-0000997-T02-IM3","P-0002647-T02-IM5","P-0002738-T02-IM5","P-0002825-T02-IM5","P-0003101-T02-IM5","P-0003101-T03-","P-0006970-T02-IM5IM5","P-0003241-T02-IM5","P-0004910-T04-IM5","P-0004954-T02-IM5","P-0005361-T02-IM5","P-0007076-T03-IM5","P-0008380-T02-IM5")))
cbioportal_genie_raw <- read.delim(file = "input_datatables/AACR_GENIE_210421.tsv", sep = "\t", header = T, stringsAsFactors = F)
cbioportal_genie <- read.delim(file = "input_datatables/AACR_GENIE_210421.tsv", sep = "\t", header = T, stringsAsFactors = F) %>% mutate(length = nchar(Protein.Change)) %>% filter(length <= 5) %>% mutate(variant = gsub("[*]","X",Protein.Change)) %>% group_by(Study, Sample.ID, Cancer.Type) %>% summarize(variant = toString(variant), .groups = "drop") %>% mutate(length = nchar(variant)) %>% filter(length <= 5)

cbioportal <- rbind(cbioportal_standard, cbioportal_genie)
cbioportal$type <- ""

cbioportal[grepl("Uterine",cbioportal$Cancer.Type),"type"] <- "uterine"
cbioportal[grepl("ervical",cbioportal$Cancer.Type),"type"] <- "uterine"
cbioportal[grepl("Endometrial",cbioportal$Cancer.Type),"type"] <- "uterine"
cbioportal[grepl("Breast",cbioportal$Cancer.Type),"type"] <- "breast"
cbioportal[grepl("Glio",cbioportal$Cancer.Type),"type"] <- "brain"
cbioportal[grepl("Astro",cbioportal$Cancer.Type),"type"] <- "brain"
cbioportal[grepl("Medulloblastoma",cbioportal$Cancer.Type),"type"] <- "brain"
cbioportal[grepl("Brain",cbioportal$Cancer.Type),"type"] <- "brain"
cbioportal[grepl("Neuroblastoma",cbioportal$Cancer.Type),"type"] <- "brain"
cbioportal[grepl("glioma",cbioportal$Cancer.Type),"type"] <- "brain"
cbioportal[grepl("Ganglioneuroblastoma",cbioportal$Cancer.Type),"type"] <- "brain"
cbioportal[grepl("Dysembryoplastic Neuroepithelial Tumor",cbioportal$Cancer.Type),"type"] <- "brain"
cbioportal[grepl("Lung",cbioportal$Cancer.Type),"type"] <- "lung"
cbioportal[grepl("Alveolar",cbioportal$Cancer.Type),"type"] <- "lung"
cbioportal[grepl("Colorectal",cbioportal$Cancer.Type),"type"] <- "colorectal"
cbioportal[grepl("Colon",cbioportal$Cancer.Type),"type"] <- "colorectal"
cbioportal[grepl("Anal",cbioportal$Cancer.Type),"type"] <- "colorectal"
cbioportal[grepl("Rectal",cbioportal$Cancer.Type),"type"] <- "colorectal"
cbioportal[grepl("Bowel",cbioportal$Cancer.Type),"type"] <- "colorectal"
cbioportal[grepl("Prostate",cbioportal$Cancer.Type),"type"] <- "prostate"
cbioportal[grepl("Melanoma",cbioportal$Cancer.Type),"type"] <- "skin"
cbioportal[grepl("Cutaneous",cbioportal$Cancer.Type),"type"] <- "skin"
cbioportal[grepl("Skin",cbioportal$Cancer.Type),"type"] <- "skin"
cbioportal[grepl("Merkel",cbioportal$Cancer.Type),"type"] <- "skin"
cbioportal[grepl("Pleural Mesothelioma",cbioportal$Cancer.Type),"type"] <- "skin"

cbioportal[grepl("Uterine",cbioportal$Study),"type"] <- "uterine"
cbioportal[grepl("Endometrial",cbioportal$Study),"type"] <- "uterine"
cbioportal[grepl("Breast",cbioportal$Study),"type"] <- "breast"
cbioportal[grepl("Glio",cbioportal$Study),"type"] <- "brain"
cbioportal[grepl("Brain",cbioportal$Study),"type"] <- "brain"
cbioportal[grepl("GBM",cbioportal$Study),"type"] <- "brain"
cbioportal[grepl("Medulloblastoma",cbioportal$Study),"type"] <- "brain"
cbioportal[grepl("Lung",cbioportal$Study),"type"] <- "lung"
cbioportal[grepl("Non-Small Cell Cancer",cbioportal$Study),"type"] <- "lung"
cbioportal[grepl("Colo",cbioportal$Study),"type"] <- "colorectal"
cbioportal[grepl("Rectal",cbioportal$Study),"type"] <- "colorectal"
cbioportal[grepl("Anorectal",cbioportal$Study),"type"] <- "colorectal"
cbioportal[grepl("Prostate",cbioportal$Study),"type"] <- "prostate"
cbioportal[grepl("prostate",cbioportal$Study),"type"] <- "prostate"
cbioportal[grepl("Melanoma",cbioportal$Study),"type"] <- "skin"
cbioportal[grepl("Cutaneous",cbioportal$Study),"type"] <- "skin"
cbioportal[grepl("Skin",cbioportal$Study),"type"] <- "skin"

cbioportal_annotated <- cbioportal %>% select(Sample.ID, Cancer.Type, variant, length, type) %>% distinct()
cbioportal_remaining <- cbioportal_annotated %>% filter(type == "")
cbioportal_remaining2 <- data.frame(table(cbioportal_remaining$Cancer.Type)) %>% arrange(desc(Freq))

uterine <- cbioportal_annotated %>% filter(type == "uterine") #1019
breast <- cbioportal_annotated %>% filter(type == "breast") #628
brain <- cbioportal_annotated %>% filter(type == "brain") #1197
lung <- cbioportal_annotated %>% filter(type == "lung") #480
colorectal <- cbioportal_annotated %>% filter(type == "colorectal") #472
prostate <- cbioportal_annotated %>% filter(type == "prostate") #204
skin <- cbioportal_annotated %>% filter(type == "skin") #355
remaining <- cbioportal_annotated %>% filter(type == "") #987

tcga_rbind <- rbind(brain, colorectal, prostate, breast, skin, lung, uterine, remaining)

uterine_table <- data.frame(table((tcga_rbind %>% filter(type == "uterine"))$variant))
breast_table <- data.frame(table((tcga_rbind %>% filter(type == "breast"))$variant))
brain_table <- data.frame(table((tcga_rbind %>% filter(type == "brain"))$variant))
lung_table <- data.frame(table((tcga_rbind %>% filter(type == "lung"))$variant))
colorectal_table <- data.frame(table((tcga_rbind %>% filter(type == "colorectal"))$variant))
prostate_table <- data.frame(table((tcga_rbind %>% filter(type == "prostate"))$variant))
skin_table <- data.frame(table((tcga_rbind %>% filter(type == "skin"))$variant))
remaining <- data.frame(table((tcga_rbind %>% filter(type == ""))$variant))

tcga_merge <- merge(data.frame("variant" = breast_table$Var1, "breast" = breast_table$Freq),
                    data.frame("variant" = uterine_table$Var1, "uterine" = uterine_table$Freq), by = "variant",all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = colorectal_table$Var1, "colorectal" = colorectal_table$Freq), by = "variant", all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = lung_table$Var1, "lung" = lung_table$Freq), by = "variant", all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = skin_table$Var1, "skin" = skin_table$Freq), by = "variant", all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = brain_table$Var1, "brain" = brain_table$Freq), by = "variant", all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = prostate_table$Var1, "prostate" = prostate_table$Freq), by = "variant", all = T)
tcga_merge <- merge(tcga_merge, data.frame("variant" = remaining$Var1, "remaining" = remaining$Freq), by = "variant", all = T)
```

``` r
complete_abund_act2 <- complete_abund_act %>% filter(snv == 1) %>% mutate(position = gsub("[A-Z]","",variant) ,end = substr(gsub("[0-9]","",variant),2,2)) %>% mutate(abund_act_class = as.character(abund_act_class))
complete_abund_act2[complete_abund_act2$position %in% seq(1,350,1) & complete_abund_act2$end == "X","abund_act_class"] <- "3_loss_of_both"   ## Calling nonsense variants in structured regions as "loss of both"
complete_abund_act2[complete_abund_act2$variant %in% c("R130G","G129E","R130Q","C124S"),"abund_act_class"] <- "4_loss_of_activity_only"

abund_act_tcga <- merge(complete_abund_act2[,c("variant","abund_act_class")],tcga_merge, by = "variant", all = T) %>% mutate(count = 1)
abund_act_tcga[abund_act_tcga$variant %in% c("T319X","Y68H","L152X","V53X","M198X","F104X","V343X","L108X","D109X","F258X","F341X","H93X"),"abund_act_class"] <- "3_loss_of_both"
abund_act_tcga[abund_act_tcga$variant %in% c("R130Q"),"abund_act_class"] <- "4_loss_of_activity_only"
abund_act_tcga[is.na(abund_act_tcga)] <- 0
abund_act_tcga[abund_act_tcga$abund_act_class == 0,"abund_act_class"] <- "NA"

### Make a second abund act class to after subtracting out 
abund_act_tcga$abund_act_class2 <- NA

for(x in 1:nrow(abund_act_tcga)){
  if(abund_act_tcga$abund_act_class[x] == "4_loss_of_activity_only"){
    if(abund_act_tcga$variant[x] %in% c("R130G","G129E","R130Q","C124S")){abund_act_tcga$abund_act_class2[x] <- "5_known_dominant_negative"} else{abund_act_tcga$abund_act_class2[x] <- "6_other_loss_of_activity_only"}
  } else{abund_act_tcga$abund_act_class2[x] <- abund_act_tcga$abund_act_class[x]}
}

## Now to make the left side of the figure, and count the number of variants in each category
abund_act_tcga_summary <- abund_act_tcga %>% group_by(abund_act_class) %>% summarize(possible = sum(count), breast = sum(breast), uterine = sum(uterine), colorectal = sum(colorectal), lung = sum(lung), skin = sum(skin), brain = sum(brain), prostate = sum(prostate), remaining = sum(remaining), .groups = "drop")

#### 
paste("Total number of uterine cancer PTEN variant analyzed:",sum(abund_act_tcga_summary[abund_act_tcga_summary$abund_act_class %in% c("1_wt_like","2_loss_of_abundance_only","3_loss_of_both","4_loss_of_activity_only"),"uterine"]))
```

    ## [1] "Total number of uterine cancer PTEN variant analyzed: 610"

``` r
paste("Total number of breast cancer PTEN variant analyzed:",sum(abund_act_tcga_summary[abund_act_tcga_summary$abund_act_class %in% c("1_wt_like","2_loss_of_abundance_only","3_loss_of_both","4_loss_of_activity_only"),"breast"]))
```

    ## [1] "Total number of breast cancer PTEN variant analyzed: 303"

``` r
paste("Total number of brain cancer PTEN variant analyzed:",sum(abund_act_tcga_summary[abund_act_tcga_summary$abund_act_class %in% c("1_wt_like","2_loss_of_abundance_only","3_loss_of_both","4_loss_of_activity_only"),"brain"]))
```

    ## [1] "Total number of brain cancer PTEN variant analyzed: 411"

``` r
paste("Total number of colorectal cancer PTEN variant analyzed:",sum(abund_act_tcga_summary[abund_act_tcga_summary$abund_act_class %in% c("1_wt_like","2_loss_of_abundance_only","3_loss_of_both","4_loss_of_activity_only"),"colorectal"]))
```

    ## [1] "Total number of colorectal cancer PTEN variant analyzed: 191"

``` r
paste("Total number of lung cancer PTEN variant analyzed:",sum(abund_act_tcga_summary[abund_act_tcga_summary$abund_act_class %in% c("1_wt_like","2_loss_of_abundance_only","3_loss_of_both","4_loss_of_activity_only"),"lung"]))
```

    ## [1] "Total number of lung cancer PTEN variant analyzed: 205"

``` r
paste("Total number of prostate cancer PTEN variant analyzed:",sum(abund_act_tcga_summary[abund_act_tcga_summary$abund_act_class %in% c("1_wt_like","2_loss_of_abundance_only","3_loss_of_both","4_loss_of_activity_only"),"prostate"]))
```

    ## [1] "Total number of prostate cancer PTEN variant analyzed: 98"

``` r
paste("Total number of skin cancer PTEN variant analyzed:",sum(abund_act_tcga_summary[abund_act_tcga_summary$abund_act_class %in% c("1_wt_like","2_loss_of_abundance_only","3_loss_of_both","4_loss_of_activity_only"),"skin"]))
```

    ## [1] "Total number of skin cancer PTEN variant analyzed: 122"

``` r
paste("Total number of remaining cancer PTEN variant analyzed:",sum(abund_act_tcga_summary[abund_act_tcga_summary$abund_act_class %in% c("1_wt_like","2_loss_of_abundance_only","3_loss_of_both","4_loss_of_activity_only"),"remaining"]))
```

    ## [1] "Total number of remaining cancer PTEN variant analyzed: 406"

``` r
colSums(abund_act_tcga_summary[1:4,2:ncol(abund_act_tcga_summary)])
```

    ##   possible     breast    uterine colorectal       lung       skin      brain 
    ##        850        303        610        191        205        122        411 
    ##   prostate  remaining 
    ##         98        406

``` r
abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)] <- t(t(abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)]) / colSums(abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)]))
colSums(abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)])
```

    ##   possible     breast    uterine colorectal       lung       skin      brain 
    ##          1          1          1          1          1          1          1 
    ##   prostate  remaining 
    ##          1          1

``` r
abund_act_tcga_summary <- abund_act_tcga_summary %>%  filter(abund_act_class != "NA") 
abund_act_tcga_summary_melt <- melt(as.data.frame(abund_act_tcga_summary), id = "abund_act_class") %>% filter(variable %in% c("possible","uterine","breast","brain","colorectal","lung","prostate","skin","remaining"))
abund_act_tcga_summary_melt$variable <- factor(abund_act_tcga_summary_melt$variable, levels = c("possible","uterine","breast","brain","colorectal","lung","prostate","skin","remaining"))

Cancer_genomics_plot1.pdf = ggplot() + 
  theme_bw() + 
  theme(panel.grid.major.x = element_blank(), axis.text.x = element_text(angle = 0, hjust = 0.5, vjust = 0.5)) +
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

## Now to make the right side of the figure, and count the number of variants in each category
abund_act_tcga_summary2 <- abund_act_tcga %>% group_by(abund_act_class2) %>% summarize(possible = sum(count), breast = sum(breast), uterine = sum(uterine), colorectal = sum(colorectal), lung = sum(lung), skin = sum(skin), brain = sum(brain), prostate = sum(prostate), remaining = sum(remaining), .groups = "drop")

colSums(abund_act_tcga_summary2[1:4,2:ncol(abund_act_tcga_summary2)])
```

    ##   possible     breast    uterine colorectal       lung       skin      brain 
    ##        812        275        557        190        193        116        386 
    ##   prostate  remaining 
    ##         95        382

``` r
abund_act_tcga_summary2[,2:ncol(abund_act_tcga_summary2)] <- t(t(abund_act_tcga_summary2[,2:ncol(abund_act_tcga_summary2)]) / colSums(abund_act_tcga_summary2[,2:ncol(abund_act_tcga_summary2)]))
colSums(abund_act_tcga_summary2[,2:ncol(abund_act_tcga_summary2)])
```

    ##   possible     breast    uterine colorectal       lung       skin      brain 
    ##          1          1          1          1          1          1          1 
    ##   prostate  remaining 
    ##          1          1

``` r
abund_act_tcga_summary2 <- abund_act_tcga_summary2 %>% filter(abund_act_class2 %in% c("5_known_dominant_negative","6_other_loss_of_activity_only")) 
abund_act_tcga_summary_melt2 <- melt(as.data.frame(abund_act_tcga_summary2), id = "abund_act_class2") %>% filter(variable %in% c("possible","uterine","breast","brain","colorectal","lung","prostate","skin","remaining"))
abund_act_tcga_summary_melt2$variable <- factor(abund_act_tcga_summary_melt2$variable, levels = c("possible","uterine","breast","brain","colorectal","lung","prostate","skin","remaining"))

Cancer_genomics_plot2.pdf = ggplot() + 
  theme_bw() + 
  theme(panel.grid.major.x = element_blank(), axis.text.x = element_text(angle = 0, hjust = 0.5, vjust = 0.5)) +
  xlab(NULL) + ylab("Fraction of observed variants") +
  scale_y_log10(limits = c(0.001,1)) +
  geom_hline(yintercept = 1, linetype = 2) +
  geom_point(data = subset(abund_act_tcga_summary_melt2, variable != "possible"), aes(x = abund_act_class2, y = value, color = variable), position=position_dodge(width=0.7), alpha = 1) +
  geom_point(data = subset(abund_act_tcga_summary_melt2, variable == "possible"), aes(x = abund_act_class2, y = value), shape = 95, size = 30, alpha = 0.5)
Cancer_genomics_plot2.pdf
```

![](PTEN_composite_analysis_files/figure-gfm/TCGA%20plot-2.png)<!-- -->

``` r
ggsave(file = "plots/Cancer_genomics_plot2.pdf", Cancer_genomics_plot2.pdf, height = 40, width = 80, units = "mm")
```

``` r
complete_abund_act2 <- complete_abund_act %>% filter(snv == 1) %>% mutate(position = gsub("[A-Z]","",variant) ,end = substr(gsub("[0-9]","",variant),2,2)) %>% mutate(abund_act_class = as.character(abund_act_class))
complete_abund_act2[complete_abund_act2$position %in% seq(1,350,1) & complete_abund_act2$end == "X","abund_act_class"] <- "3_loss_of_both"   ## Calling nonsense variants in structured regions as "loss of both"

complete_abund_act2[complete_abund_act2$abund_act_class == "4_loss_of_activity_only","abund_act_class"] <- "6_other_loss_of_activity_only"
complete_abund_act2[complete_abund_act2$variant %in% c("R130G","G129E","R130Q","C124S"),"abund_act_class"] <- "5_known_dominant_negative"

abund_act_tcga <- merge(complete_abund_act2[,c("variant","abund_act_class")],tcga_merge, by = "variant", all = T) %>% mutate(count = 1)
abund_act_tcga[abund_act_tcga$variant %in% c("T319X","Y68H","L152X","V53X","M198X","F104X","V343X","L108X","D109X","F258X","F341X","H93X"),"abund_act_class"] <- "3_loss_of_both"
abund_act_tcga[abund_act_tcga$variant %in% c("R130Q"),"abund_act_class"] <- "5_known_dominant_negative"
abund_act_tcga[is.na(abund_act_tcga)] <- 0
abund_act_tcga[abund_act_tcga$abund_act_class == 0,"abund_act_class"] <- "NA"

abund_act_tcga_summary <- abund_act_tcga %>% group_by(abund_act_class) %>% summarize(possible = sum(count), breast = sum(breast), uterine = sum(uterine), colorectal = sum(colorectal), lung = sum(lung), skin = sum(skin), brain = sum(brain), prostate = sum(prostate), remaining = sum(remaining), .groups = "drop")

## Let's count the number of variants in each category
colSums(abund_act_tcga_summary[1:4,2:ncol(abund_act_tcga_summary)])
```

    ##   possible     breast    uterine colorectal       lung       skin      brain 
    ##        812        275        557        190        193        116        386 
    ##   prostate  remaining 
    ##         95        382

``` r
abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)] <- t(t(abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)]) / colSums(abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)]))
colSums(abund_act_tcga_summary[,2:ncol(abund_act_tcga_summary)])
```

    ##   possible     breast    uterine colorectal       lung       skin      brain 
    ##          1          1          1          1          1          1          1 
    ##   prostate  remaining 
    ##          1          1

``` r
abund_act_tcga_summary2 <- abund_act_tcga_summary %>%  filter(abund_act_class != "NA") 

abund_act_tcga_summary_melt <- melt(as.data.frame(abund_act_tcga_summary2), id = "abund_act_class") %>% filter(variable %in% c("possible","uterine","breast","brain","colorectal","lung","prostate","skin","remaining"))

abund_act_tcga_summary_melt$variable <- factor(abund_act_tcga_summary_melt$variable, levels = c("possible","uterine","breast","brain","colorectal","lung","prostate","skin","remaining"))

abund_act_tcga_summary_melt2 <- abund_act_tcga_summary_melt %>% filter(abund_act_class %in% c("5_known_dominant_negative","6_other_loss_of_activity_only"))

Cancer_genomics_plot2.pdf = ggplot() + 
  theme_bw() + 
  theme(panel.grid.major.x = element_blank(), axis.text.x = element_text(angle = 0, hjust = 0.5, vjust = 0.5)) +
  xlab(NULL) + ylab("Fraction of observed variants") +
  scale_y_log10(limits = c(0.001,1)) +
  geom_hline(yintercept = 1, linetype = 2) +
  geom_point(data = subset(abund_act_tcga_summary_melt2, variable != "possible"), aes(x = abund_act_class, y = value, color = variable), position=position_dodge(width=0.7), alpha = 1) +
  geom_point(data = subset(abund_act_tcga_summary_melt2, variable == "possible"), aes(x = abund_act_class, y = value), shape = 95, size = 30, alpha = 0.5)
Cancer_genomics_plot2.pdf
```

![](PTEN_composite_analysis_files/figure-gfm/TCGA%20plot2%20where%20the%20loss%20of%20activity%20only%20variants%20are%20subdivided-1.png)<!-- -->

``` r
ggsave(file = "plots/Cancer_genomics_plot2.pdf", Cancer_genomics_plot2.pdf, height = 40, width = 80, units = "mm")

stable_inactive_tcga <- abund_act_tcga %>% filter(abund_act_class == "6_other_loss_of_activity_only") %>% arrange(desc(breast, uterine))
stable_inactive_to_test <- complete_abund_act_missense %>% filter(variant %in% c("R130P","D92H","D24G","R159S","Y46D","Y16S","T160P"))
stable_inactive_to_test2 <- merge(stable_inactive_to_test, stable_inactive_tcga[,c("variant","breast","uterine")], by = "variant", all.x = T)

### Also, quantifying what fraction of the enrichment of the loss-of-activity only variants is due ot the known dominant negatives
paste("Fraction of breast cancer loss-of-activity only variants accounted for by known dom negs:",round(abund_act_tcga_summary2[abund_act_tcga_summary2$abund_act_class == "5_known_dominant_negative","breast"] / (abund_act_tcga_summary2[abund_act_tcga_summary2$abund_act_class == "5_known_dominant_negative","breast"] + abund_act_tcga_summary2[abund_act_tcga_summary2$abund_act_class == "6_other_loss_of_activity_only","breast"]),2))
```

    ## [1] "Fraction of breast cancer loss-of-activity only variants accounted for by known dom negs: 0.63"

``` r
paste("Fraction of uterine cancer loss-of-activity only variants accounted for by known dom negs:",round(abund_act_tcga_summary2[abund_act_tcga_summary2$abund_act_class == "5_known_dominant_negative","uterine"] / (abund_act_tcga_summary2[abund_act_tcga_summary2$abund_act_class == "5_known_dominant_negative","uterine"] + abund_act_tcga_summary2[abund_act_tcga_summary2$abund_act_class == "6_other_loss_of_activity_only","uterine"]),2))
```

    ## [1] "Fraction of uterine cancer loss-of-activity only variants accounted for by known dom negs: 0.83"

``` r
paste("Fraction of lung cancer loss-of-activity only variants accounted for by known dom negs:",round(abund_act_tcga_summary2[abund_act_tcga_summary2$abund_act_class == "5_known_dominant_negative","lung"] / (abund_act_tcga_summary2[abund_act_tcga_summary2$abund_act_class == "5_known_dominant_negative","lung"] + abund_act_tcga_summary2[abund_act_tcga_summary2$abund_act_class == "6_other_loss_of_activity_only","lung"]),2))
```

    ## [1] "Fraction of lung cancer loss-of-activity only variants accounted for by known dom negs: 0.71"

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
  theme_bw() + theme(panel.grid.minor = element_blank()) +
  geom_text_repel(data = subset(pakt_merged, !(variant %in% c("WT","none"))), aes(x = pakt, y = total_cancer_count, label = variant), color = "red", segment.colour = "orange") +
  geom_point(data = subset(pakt_merged, !(variant %in% c("WT","none"))), aes(x = pakt, y = total_cancer_count)) +
  xlab("Normalized Akt1 pT308 by western blot") + 
  ylab("Total number of variants observed in TCGA") +
  scale_x_log10(limits = c(0.5,12.5)) +
  geom_vline(xintercept = 1, linetype = 2, alpha = 0.5)
pAkt_vs_TCGA_count_plot
```

![](PTEN_composite_analysis_files/figure-gfm/pAKT%20vs%20cancer%20counts-1.png)<!-- -->

``` r
ggsave(file = "plots/pAkt_vs_TCGA_count_plot.pdf", pAkt_vs_TCGA_count_plot, height = 60, width = 100, units = "mm")

paste("The Pearson's r of the TCGA variant count and pAKT level scored in our western blot:",round(cor(pakt_merged$pakt, pakt_merged$total_cancer_count, method = "pearson"),2))
```

    ## [1] "The Pearson's r of the TCGA variant count and pAKT level scored in our western blot: 0.8"

``` r
ccle_muts <- read.csv(file = "input_datatables/CCLE_PTEN_mutations.csv", header = T, stringsAsFactors = FALSE)
ccle_rppa <- read.csv(file = "input_datatables/CCLE_RPPA_20181003.csv", header = T, stringsAsFactors = FALSE)

ccle_short <- ccle_rppa[,c("X","Akt_pT308","PTEN")]
for(x in 1:nrow(ccle_short)){ccle_short$Cell.Line[x] <- strsplit(ccle_short$X[x], "_")[[1]][1]}

ccle_muts_missense <- ccle_muts %>% filter(Variant.Classification == "Missense_Mutation") 
ccle_muts_missense_single <- ccle_muts_missense %>% mutate(number = 1) %>% group_by(Cell.Line) %>% summarize(number = sum(number)) %>% filter(number == 1)
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

``` r
other_loss_of_activity <- abund_act_tcga %>% filter(abund_act_class == "6_other_loss_of_activity_only")

other_loss_of_activity_expected_domneg <- other_loss_of_activity %>% filter(variant %in% c("R130P","R130L","D92A","D92E","D92H"))

paste("Fraction of uncharacterized loss of activity only variants that may be dominant negatives:", round(nrow(other_loss_of_activity_expected_domneg) / nrow(other_loss_of_activity),2))
```

    ## [1] "Fraction of uncharacterized loss of activity only variants that may be dominant negatives: 0.13"

``` r
variant_abund_act_class_table <- complete_abund_act %>% select(variant, abund_act_class)

combined2 <- merge(combined[,c("variant","se_total")], variant_abund_act_class_table, by = "variant") %>% mutate(count = 1)

combined2_summary <- combined2 %>% group_by(abund_act_class) %>% summarize(mean_se = mean(se_total), count = sum(count), .groups = "drop")
```

``` r
cbioportal_raw2 <- cbioportal_raw[,c("Sample.ID","Protein.Change", "Allele.Freq..T.")]
cbioportal_genie_raw2 <- cbioportal_genie_raw[,c("Sample.ID","Protein.Change", "Allele.Freq..T.")]
for(x in 1:nrow(cbioportal_genie_raw2)){
  if(substr(cbioportal_genie_raw2$Sample.ID[x],1,10) == "GENIE-MSK-"){
    cbioportal_genie_raw2$Sample.ID[x] <- substr(cbioportal_genie_raw2$Sample.ID[x],11,30)}
}

cbioportal_combined_raw2 <- rbind(cbioportal_raw2,cbioportal_genie_raw2) %>% distinct()
colnames(cbioportal_combined_raw2) <- c("sample","variant","allele_frac")
cbioportal_combined_raw2$variant <- gsub("[*]","X",cbioportal_combined_raw2$variant)

cbioportal_combined_raw3 <- merge(cbioportal_combined_raw2, abund_act_tcga[,c("variant","abund_act_class")], by = "variant")

cbioportal_combined_raw3_combined <- data.frame(sample = unique(cbioportal_combined_raw2$sample), allele1 = NA, allele1_frac = NA,  allele1_type = NA, allele2 = NA, allele2_frac = NA, allele2_type = NA)
for(x in 1:nrow(cbioportal_combined_raw3_combined)){
  temp <- subset(cbioportal_combined_raw3, sample == cbioportal_combined_raw3$sample[x])
  if(nrow(temp) == 1){
    cbioportal_combined_raw3_combined$allele1[x] <- temp$variant[1]
    cbioportal_combined_raw3_combined$allele1_frac[x] <- temp$allele_frac[1]
    cbioportal_combined_raw3_combined$allele1_type[x] <- temp$abund_act_class[1]}
  if(nrow(temp) == 2 & (temp$variant[1] == temp$variant[2])){
    cbioportal_combined_raw3_combined$allele1[x] <- temp$variant[1]
    cbioportal_combined_raw3_combined$allele1_frac[x] <- temp$allele_frac[1]
    cbioportal_combined_raw3_combined$allele1_type[x] <- temp$abund_act_class[1]}
  if(nrow(temp) == 2 & (temp$variant[1] != temp$variant[2])){
    cbioportal_combined_raw3_combined$allele1[x] <- temp$variant[1]
    cbioportal_combined_raw3_combined$allele1_frac[x] <- temp$allele_frac[1]
    cbioportal_combined_raw3_combined$allele1_type[x] <- temp$abund_act_class[1]
    cbioportal_combined_raw3_combined$allele2[x] <- temp$variant[2]
    cbioportal_combined_raw3_combined$allele2_frac[x] <- temp$allele_frac[2]
    cbioportal_combined_raw3_combined$allele2_type[x] <- temp$abund_act_class[2]}
}

cbioportal_combined_raw3_combined$wt_frac <- 1 - rowSums(cbioportal_combined_raw3_combined[,c("allele1_frac","allele2_frac")], na.rm = T)

cbioportal_types <- c("1_wt_like","2_loss_of_abundance_only","3_loss_of_both","4_loss_of_activity_only","5_known_dominant_negative","6_other_loss_of_activity_only")

cbioportal_combined_raw3_combined_complete <- cbioportal_combined_raw3_combined %>% filter(allele1_type %in% cbioportal_types & !is.na(allele1_frac))
cbioportal_combined_raw3_combined_complete2 <- cbioportal_combined_raw3_combined_complete[nchar(cbioportal_combined_raw3_combined_complete$allele2_type) != 2 | is.na(cbioportal_combined_raw3_combined_complete$allele2_type),]

nrow(cbioportal_combined_raw3_combined_complete2 %>% filter(is.na(allele2)))
```

    ## [1] 1944

``` r
nrow(cbioportal_combined_raw3_combined_complete2 %>% filter(!is.na(allele2)))
```

    ## [1] 252

``` r
nrow(cbioportal_combined_raw3_combined_complete2 %>% filter(wt_frac < 0.1))
```

    ## [1] 40

``` r
nrow(cbioportal_combined_raw3_combined_complete2 %>% filter(wt_frac < 0.5))
```

    ## [1] 711

``` r
cbioportal_combined_raw3_combined_complete2_melt <- melt(cbioportal_combined_raw3_combined_complete2[,c("sample","allele1_frac","allele2_frac","wt_frac")], id = "sample")
cbioportal_combined_raw3_combined_complete2_melt$variable <- as.character(cbioportal_combined_raw3_combined_complete2_melt$variable)

cbioportal_combined_raw3_combined_complete2_melt[cbioportal_combined_raw3_combined_complete2_melt$variable == "wt_frac","variable"] <- "(1) WT"
cbioportal_combined_raw3_combined_complete2_melt[cbioportal_combined_raw3_combined_complete2_melt$variable == "allele1_frac","variable"] <- "(2) Variant 1"
cbioportal_combined_raw3_combined_complete2_melt[cbioportal_combined_raw3_combined_complete2_melt$variable == "allele2_frac","variable"] <- "(3) Variant 2"

Allele_fraction_in_cancer_data <- ggplot() + scale_x_continuous(limits = c(0,1)) + labs(x = "Number of samples", y = "Allele fraction in sample") +
  geom_histogram(data = cbioportal_combined_raw3_combined_complete2_melt, aes(x = value), alpha = 0.5, binwidth = 0.05) +
  facet_grid(rows = vars(variable))
ggsave(file = "plots/Allele_fraction_in_cancer_data.pdf", Allele_fraction_in_cancer_data, height = 3, width = 6)
```

    ## Warning: Removed 1948 rows containing non-finite values (stat_bin).

    ## Warning: Removed 6 rows containing missing values (geom_bar).

``` r
median(cbioportal_combined_raw3_combined_complete2$allele1_frac)
```

    ## [1] 0.33

``` r
median(cbioportal_combined_raw3_combined_complete2$allele2_frac, na.rm = T)
```

    ## [1] 0.275

``` r
cbioportal_combined_raw3_combined_complete3 <- cbioportal_combined_raw3_combined_complete2 %>% mutate(count = 1) #%>% filter(allele1_type %in% c("1_wt_like","3_loss_of_both","5_known_dominant_negative","6_other_loss_of_activity_only") & allele2_type %in% c("1_wt_like","3_loss_of_both","5_known_dominant_negative","6_other_loss_of_activity_only")) 

cbioportal_combined_raw3_combined_complete3[is.na(cbioportal_combined_raw3_combined_complete3$allele2_type),"allele2_type"] <- "1_wt_like"
cbioportal_combined_raw3_combined_complete3[is.na(cbioportal_combined_raw3_combined_complete3$allele2_frac),"allele2_frac"] <- 0

cbioportal_combined_raw3_combined_complete3[cbioportal_combined_raw3_combined_complete3$allele1_type == "5_known_dominant_negative","allele1_type"] <- "4_loss_of_activity_only"
cbioportal_combined_raw3_combined_complete3[cbioportal_combined_raw3_combined_complete3$allele2_type == "5_known_dominant_negative","allele2_type"] <- "4_loss_of_activity_only"
cbioportal_combined_raw3_combined_complete3[cbioportal_combined_raw3_combined_complete3$allele1_type == "6_other_loss_of_activity_only","allele1_type"] <- "4_loss_of_activity_only"
cbioportal_combined_raw3_combined_complete3[cbioportal_combined_raw3_combined_complete3$allele2_type == "6_other_loss_of_activity_only","allele2_type"] <- "4_loss_of_activity_only"

wt_fraction_by_variant_class <- cbioportal_combined_raw3_combined_complete3 %>% group_by(allele1_type, allele2_type) %>% summarize(allele1_frac = mean(allele1_frac), allele2_frac = mean(allele2_frac), wt_frac = mean(wt_frac), count = sum(count), .groups = "drop")

ggplot() + theme(axis.text.x = element_text(angle = -90, hjust = 0, vjust = 0.5)) + 
  geom_tile(data = wt_fraction_by_variant_class, aes(x = allele1_type, y = allele2_type, fill = wt_frac))
```

![](PTEN_composite_analysis_files/figure-gfm/Allele%20frequencies%20in%20cancer-1.png)<!-- -->

``` r
tumors_of_single_classes <- cbioportal_combined_raw3_combined_complete3 %>% filter(allele1_type == allele2_type) %>% mutate(variant_frac  = allele1_frac+ allele2_frac)

tumors_of_single_classes2 <- tumors_of_single_classes %>% group_by(allele1_type) %>% summarize(variant_frac = sum(variant_frac), count = sum(count), .groups = "drop")
```

``` r
## Comparing the 2000 Han Ishioka CancerRes activity data to the yeast functional assay
han_ishioka <- read.csv(file = "input_datatables/2000_Han_Ishioka_PTEN_activity.csv")

han_ishioka2 <- merge(han_ishioka, complete_abund_act_missense2, by = "variant", all.x = T)

han_ishioka2[han_ishioka2$variant == "WT","score_abundance"] <- 1
han_ishioka2[han_ishioka2$variant == "NULL","score_abundance"] <- 0
han_ishioka2[han_ishioka2$variant == "WT","score_activity"] <- 1

han_ishioka3 <- han_ishioka2 %>% group_by(variant) %>% summarize(mean_abundance = mean(score_abundance), mean_invitro_activity = mean(value), mean_yeast_activity = mean(score_activity), .groups = "drop") %>% filter(!is.na(mean_abundance) & !is.na(mean_invitro_activity) & !is.na(mean_yeast_activity) & !(variant %in% c("R130G","R130L")))

ggplot() + scale_y_log10() + scale_x_continuous() +
  labs(x = "Yeast activity score", y = "In vitro activity") + 
  geom_hline(yintercept = max(subset(han_ishioka3, (variant %in% c("NULL")))$value), linetype = 2, color = "black", alpha = 0.5) +
  geom_vline(xintercept = activity_syn_5th, linetype = 2, color = "red", alpha = 0.5) +
  geom_vline(xintercept = activity_nonsense_5th, linetype = 2, color = "blue", alpha = 0.5) +
  geom_point(data = subset(han_ishioka3, !(variant %in% c("WT","NULL"))), aes(x = mean_yeast_activity, y = mean_invitro_activity)) +
  geom_text_repel(data = subset(han_ishioka3, !(variant %in% c("WT","NULL"))), aes(x = mean_yeast_activity, y = mean_invitro_activity, label = variant), color = "red")
```

    ## Warning: Unknown or uninitialised column: `value`.

    ## Warning in max(subset(han_ishioka3, (variant %in% c("NULL")))$value): no non-
    ## missing arguments to max; returning -Inf

    ## Warning in log(x, base): NaNs produced

    ## Warning: Removed 1 rows containing missing values (geom_hline).

![](PTEN_composite_analysis_files/figure-gfm/Extra-1.png)<!-- -->

``` r
ggplot() + scale_y_log10() + scale_x_continuous() +
  labs(x = "Abundance score", y = "In vitro activity") + 
  geom_hline(yintercept = max(subset(han_ishioka3, (variant %in% c("NULL")))$value), linetype = 2, color = "black", alpha = 0.5) +
  geom_vline(xintercept = quantile(subset(complete_abund_act_missense, abundance_class == "wt-like")$score_abundance,0.01, na.rm = T), linetype = 2, color = "red", alpha = 0.5) +
  geom_vline(xintercept = quantile(subset(complete_abund_act_missense, abundance_class == "low")$score_abundance,0.99), linetype = 2, color = "blue", alpha = 0.5) +
  geom_point(data = subset(han_ishioka3, !(variant %in% c("WT","NULL"))), aes(x = mean_abundance, y = mean_invitro_activity)) +
  geom_text_repel(data = subset(han_ishioka3, !(variant %in% c("WT","NULL"))), aes(x = mean_abundance, y = mean_invitro_activity, label = variant), color = "red")
```

    ## Warning: Unknown or uninitialised column: `value`.

    ## Warning in max(subset(han_ishioka3, (variant %in% c("NULL")))$value): no non-
    ## missing arguments to max; returning -Inf

    ## Warning in log(x, base): NaNs produced

    ## Warning: Removed 1 rows containing missing values (geom_hline).

![](PTEN_composite_analysis_files/figure-gfm/Extra-2.png)<!-- -->

``` r
individual_abundance <- original %>% filter(!is.na(egfp_geomean) & !(position %in% c(seq(1,13,1),45,124,129))) 
## The first 13 residues constitute a PIP2 binding motif PMID: 25211206
## Involvement of Val45 predicted in catalysis PMID: 20538496
## Involvement of His93 in catalysis PMID: 20538496
## Cys124 is a commonly known active site residue
## Gly129 is found in the active site and mutation ablates catalysis PMID: 10597304


individual_abundance2 <- merge(individual_abundance, pten_func, by = "variant") %>% select(variant, egfp_geomean, score_activity)
individual_abundance2 <- rbind(individual_abundance2,c("WT",1,1))
individual_abundance2$egfp_geomean <- as.numeric(individual_abundance2$egfp_geomean)
individual_abundance2$score_activity <- as.numeric(individual_abundance2$score_activity)

Abundance_MFI_vs_activity_score_scatterplot <- ggplot() + 
  theme(legend.position = "none") + 
  labs(x = "Geometric mean of EGFP-PTEN MFI", y = "Activity score") + 
  scale_x_continuous(breaks = seq(0,1,0.25)) + 
  scale_y_continuous(breaks = seq(0,1,0.25), expand = c(0,0.1)) +
  geom_point(data = individual_abundance2, aes(x = egfp_geomean, y = score_activity), alpha = 0.5) +
  geom_text_repel(data = individual_abundance2, aes(x = egfp_geomean, y = score_activity, label = variant), color = "red", size = 2, force = 3, max.overlaps = getOption("ggrepel.max.overlaps", default = 20))
Abundance_MFI_vs_activity_score_scatterplot
```

    ## Warning: Removed 2 rows containing missing values (geom_point).

    ## Warning: Removed 2 rows containing missing values (geom_text_repel).

![](PTEN_composite_analysis_files/figure-gfm/Compare%20abundance%20activity-1.png)<!-- -->

``` r
ggsave(file = "Plots/Abundance_MFI_vs_activity_score_scatterplot.pdf", Abundance_MFI_vs_activity_score_scatterplot, height = 1.75, width = 3.5)
```

    ## Warning: Removed 2 rows containing missing values (geom_point).

    ## Warning: Removed 2 rows containing missing values (geom_text_repel).

``` r
low_abundance_phts <- complete_abund_act_missense2 %>% filter(abundance_class %in% c("low") & (asd == 1 | asd_dd == 1 | phts == 1 | clinvar_pathog))

table(low_abundance_phts$abund_act_class)
```

    ## 
    ## 2_loss_of_abundance_only  4_loss_of_activity_only           3_loss_of_both 
    ##                        8                        0                       22 
    ##                1_wt_like                       NA 
    ##                        0                       10

``` r
P_LP_variants_of_low_abundance_scatterplot <- ggplot() + 
  theme(legend.position = "none") + 
  labs(x = "Abundance score", y = "Activity score") + 
  scale_color_manual(values = custom_colorscale2) + 
  geom_point(data = low_abundance_phts, aes(x = score_abundance, y = score_activity, color = abund_act_class)) +
  geom_text_repel(data = low_abundance_phts %>% filter(abund_act_class != "3_loss_of_both"),
                  aes(x = score_abundance, y = score_activity, label = variant), size = 2)
P_LP_variants_of_low_abundance_scatterplot
```

![](PTEN_composite_analysis_files/figure-gfm/Seeing%20which%20PHTS%20variants%20were%20scored%20normal%20by%20the%20functional%20assay%20but%20low%20for%20abundance-1.png)<!-- -->

``` r
ggsave(file = "Plots/P_LP_variants_of_low_abundance_scatterplot.pdf", P_LP_variants_of_low_abundance_scatterplot, height = 1.75, width = 3.5)

## D252G associated with ASD and cannot rescue various molecular traits of neuronal cells (PMID: 29373119, 26579216)
## D252G, N276S, D326N - Reduced protein stability of autism-associated PTEN mutants(PMIDL 25527629)
## R173C, R173H, Y27S and R173C had reduced in-vitro phosphatase activity (PMID: 10866302)
## R173C also had reduced phosphatase activity when expressed in U87-MG Glioma cell lines (PMID: 33828082)
## K254T - Patient with K254T variant had reduced blood PTEN levels (PMID: 23066114)
## G129R - Unlike the WT allele, the G129R variant was unable to regulate cell growth when expressed in U87 and U178 Glioma cell lines (PMID: 9356475)
## P246L - Cells from a patient  heterozygous for germline P246L variant had reduced PTEN histochemistry and increased phosphorylated Akt. (PMID: 14566704)
## M134T, T202I, D252G, N276S,D326N  had reduced abundance when overexpressed in U87MG Glioma cells. (PMID: 32150788). With the exception of T202I, the rest also had reduced phosphatase activity as compared to WT when overexpressed in human cells.


## G251V observed in concurrent germ cell tumors and actue megakaryoblastic leukemia (PMID: 27148581, 24831771)
## Nothing for 6: P96A, P95T, P96S, A120E, L247S, M270K
## Existing functional evidence for 12: Y27S, G129R, M134T, R173C, R173H, T202I, P246L, G251V, D252G, K254T, N276S, D326N.
```

### Rescore the data based on codon-level information

``` r
pten_seq <- "MTAIIKEIVSRNKRRYQEDGFDLDLTYIYPNIIAMGFPAERLEGVYRNNIDDVVRFLDSKHKNHYKIYNLCAERHYDTAKFNCRVAQYPFEDHNPPQLELIKPFCEDLDQWLSEDDNHVAAIHCKAGKGRTGVMICAYLLHRGKFLKAQEALDFYGEVRTRDKKGVTIPSQRRYVYYYSYLLKNHLDYRPVALLFHKMMFETIPMFSGGTCNPQFVVCQLKVKIYSSNSGPTRREDKFMYFEFPQPLPVCGDIKVEFFHKQNKMLKKDKMFHFWVNTFFIPGPEETSEKVENGSLCDQEIDSICSIERADNDKEYLVLTLTKNDLDKANKDKANRYFSPNFKVKLYFTKTVEEPSNPEASSSTSVTPDVSDNEPDHYRYSDTTDSDPENEPFDEDQHTQITKV"

map_codon <- read.delim(file = "input_datatables/PTEN_variant_barcode_subassembly.tsv", sep = "\t", header= TRUE, stringsAsFactors = FALSE)

map_codon$aa_pos_1 <- 0
map_codon$aa_pos_2 <- 0
map_codon$aa_pos_3 <- 0
map_codon$aa_pos_4 <- 0
for(x in 1:nrow(map)){
  map_codon$aa_pos_1[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(map_codon$value[x]), " \\(p"))[2],")"))[1]))
  map_codon$aa_pos_2[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(map_codon$value[x]), " \\(p"))[3],")"))[1]))
  map_codon$aa_pos_3[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(map_codon$value[x]), " \\(p"))[4],")"))[1]))
  map_codon$aa_pos_4[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(map_codon$value[x]), " \\(p"))[5],")"))[1]))
}

## Get all unique amino acid change positions from above
map_codon$change1 <- 0
map_codon$change2 <- 0
map_codon$change3 <- 0
for(x in 1:nrow(map_codon)){
  map_codon$change1[x] <- unique(c(map_codon$aa_pos_1[x], map_codon$aa_pos_2[x], map_codon$aa_pos_3[x], map_codon$aa_pos_4[x])[c(map_codon$aa_pos_1[x], map_codon$aa_pos_2[x], map_codon$aa_pos_3[x], map_codon$aa_pos_4[x]) != ""])[1]
  map_codon$change2[x] <- unique(c(map_codon$aa_pos_1[x], map_codon$aa_pos_2[x], map_codon$aa_pos_3[x], map_codon$aa_pos_4[x])[c(map_codon$aa_pos_1[x], map_codon$aa_pos_2[x], map_codon$aa_pos_3[x], map_codon$aa_pos_4[x]) != ""])[2]
  map_codon$change3[x] <- unique(c(map_codon$aa_pos_1[x], map_codon$aa_pos_2[x], map_codon$aa_pos_3[x], map_codon$aa_pos_4[x])[c(map_codon$aa_pos_1[x], map_codon$aa_pos_2[x], map_codon$aa_pos_3[x], map_codon$aa_pos_4[x]) != ""])[3]
  if(is.na(map_codon$change1[x] & !is.na(map_codon$change2[x]))){map_codon$change1[x] <- map_codon$change2[x]}
  if(is.na(map_codon$change2[x] & map_codon$change1[x] & !is.na(map_codon$change3[x]))){map_codon$change1[x] <- map_codon$change3[x]}
}

## Find the number of mutations for each variant
map_codon$mut_number <- 0
for(x in 1:nrow(map_codon)){
  map_codon$mut_number[x] <- 3-sum(is.na(map_codon[x,c("change1","change2","change3")]))
}

##
map_codon_singles <- subset(map_codon, mut_number == 1)
map_codon_wt <- subset(map_codon, value == "_wt" & mut_number == 0)
map_codon_syn <- subset(map_codon, !is.na(value) & value != "_wt" & mut_number == 0)

map_codon_singles$start_aa3 <- "NA"
map_codon_singles$end_aa3 <- "NA"

tempy <- subset(map_codon_singles, aa_pos_1 == 1)

for(x in 1:nrow(map_codon_syn)){
  map_codon_syn$position1[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(map_codon_syn$value[x]), split = "\\(p."))[1],3,
                                                              nchar(unlist(strsplit(x = as.character(map_codon_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  map_codon_syn$position2[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(map_codon_syn$value[x]), split = "\\(p."))[2],3,
                                                              nchar(unlist(strsplit(x = as.character(map_codon_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  map_codon_syn$position3[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(map_codon_syn$value[x]), split = "\\(p."))[3],3,
                                                              nchar(unlist(strsplit(x = as.character(map_codon_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  map_codon_syn$position4[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(map_codon_syn$value[x]), split = "\\(p."))[4],3,
                                                              nchar(unlist(strsplit(x = as.character(map_codon_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  map_codon_syn$change1[x] <- unique(c(map_codon_syn$position1[x], map_codon_syn$position2[x], map_codon_syn$position3[x], map_codon_syn$position4[x])[c(map_codon_syn$position1[x], map_codon_syn$position2[x], map_codon_syn$position3[x], map_codon_syn$position4[x]) != ""])[1]
  map_codon_syn$change2[x] <- unique(c(map_codon_syn$position1[x], map_codon_syn$position2[x], map_codon_syn$position3[x], map_codon_syn$position4[x])[c(map_codon_syn$position1[x], map_codon_syn$position2[x], map_codon_syn$position3[x], map_codon_syn$position4[x]) != ""])[2]
  map_codon_syn$change3[x] <- unique(c(map_codon_syn$position1[x], map_codon_syn$position2[x], map_codon_syn$position3[x], map_codon_syn$position4[x])[c(map_codon_syn$position1[x], map_codon_syn$position2[x], map_codon_syn$position3[x], map_codon_syn$position4[x]) != ""])[3]
  map_codon_syn$start[x] <- substr(pten_seq,map_codon_syn$change1[x],map_codon_syn$change1[x])
  map_codon_syn$end[x] <- map_codon_syn$start[x]
  map_codon_syn$variant[x] <- paste(map_codon_syn$start[x],map_codon_syn$change1[x],map_codon_syn$end[x],sep="")
}
```

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

``` r
for(x in 1:nrow(map_codon_singles)){
  map_codon_singles$start_aa3[x] <- as.character(gsub("[0-9]","",substr(unlist(strsplit(x = as.character(map_codon_singles$value[x]), split = "\\(p."))[2],1,4)))
  if(map_codon_singles$start_aa3[x] == "=), "){
    map_codon_singles$start_aa3[x] <- as.character(gsub("[0-9]","",substr(unlist(strsplit(x = as.character(map_codon_singles$value[x]), split = "\\(p."))[3],1,4)))
  }
  if(map_codon_singles$start_aa3[x] == "=), "){
    map_codon_singles$start_aa3[x] <- as.character(gsub("[0-9]","",substr(unlist(strsplit(x = as.character(map_codon_singles$value[x]), split = "\\(p."))[4],1,4)))
  }
  map_codon_singles$end_aa3[x] <- substr(unlist(strsplit(x = as.character(map_codon_singles$value[x]), split = ")"))[1],nchar(unlist(strsplit(x = as.character(map_codon_singles$value[x]), split = ")"))[1]) - 2,nchar(unlist(strsplit(x = as.character(map_codon_singles$value[x]), split = ")"))[1]))
  if(map_codon_singles$end_aa3[x] == "p.="){
    map_codon_singles$end_aa3[x] <- substr(unlist(strsplit(x = as.character(map_codon_singles$value[x]), split = ")"))[2],nchar(unlist(strsplit(x = as.character(map_codon_singles$value[x]), split = ")"))[2]) - 2,nchar(unlist(strsplit(x = as.character(map_codon_singles$value[x]), split = ")"))[2]))
  }
  if(map_codon_singles$end_aa3[x] == "p.="){
    map_codon_singles$end_aa3[x] <- substr(unlist(strsplit(x = as.character(map_codon_singles$value[x]), split = ")"))[3],nchar(unlist(strsplit(x = as.character(map_codon_singles$value[x]), split = ")"))[3]) - 2,nchar(unlist(strsplit(x = as.character(map_codon_singles$value[x]), split = ")"))[3]))
  }
}

for(x in 1:nrow(map_codon_singles)){
  map_codon_singles$position[x] <- map_codon_singles$aa_pos_1[x]
  if(map_codon_singles$position[x] == "" | is.na(map_codon_singles$position[x])){
    map_codon_singles$position[x] <- map_codon_singles$aa_pos_2[x]
  }
}

map_codon_singles$start <- "NA"
map_codon_singles$end <- "NA"
map_codon_singles$variant <- "NA"

for(x in 1:nrow(map_codon_singles)){
  map_codon_singles$start[x] <- to_single_notation(map_codon_singles$start_aa3[x])
  map_codon_singles$end[x] <- to_single_notation(map_codon_singles$end_aa3[x])
  map_codon_singles$variant[x] <- paste(map_codon_singles$start[x],map_codon_singles$position[x],map_codon_singles$end[x], sep="")
}

map_codon_nonsense <- subset(map_codon_singles, end == "X")
map_codon_missense <- subset(map_codon_singles, end != "X")

map_codon_syn$position <- map_codon_syn$position1
map_codon_wt$class <- "wt"
map_codon_wt$position <- 0
map_codon_wt$start <- "Z"
map_codon_wt$end <- "Z"
map_codon_syn$class <- "syn"
map_codon_nonsense$class <- "nonsense"
map_codon_missense$class <- "missense"
map_codon_wt$variant <- "wt"

PTEN_library_variant_map_codon <- rbind(map_codon_wt[,c("barcode","value","variant","position","start","end","class")], map_codon_syn[,c("barcode","value","variant","position","start","end","class")],map_codon_nonsense[,c("barcode","value","variant","position","start","end","class")],map_codon_missense[,c("barcode","value","variant","position","start","end","class")])

#write.csv(file = "output_datatables/PTEN_library_variant_map_codon.csv", PTEN_library_variant_map_codon, row.names = FALSE, quote = FALSE)
```

``` r
e1s1_codon <- merge(e1s1_1a, e1s1_1b, by = "X", all = TRUE)
e1s1_codon <- merge(e1s1_codon, e1s1_2a, by = "X", all = TRUE)
e1s1_codon <- merge(e1s1_codon, e1s1_2b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s1_codon, e1s1_2b, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y' are duplicated in the result

``` r
e1s1_codon <- merge(e1s1_codon, e1s1_3a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s1_codon, e1s1_3a, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y' are duplicated in the result

``` r
e1s1_codon <- merge(e1s1_codon, e1s1_3b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s1_codon, e1s1_3b, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s1_codon <- merge(e1s1_codon, e1s1_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s1_codon, e1s1_4a, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s1_codon <- merge(e1s1_codon, e1s1_4b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s1_codon, e1s1_4b, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y', 'count.x', 'count.y', 'count.x', 'count.y' are
    ## duplicated in the result

``` r
colnames(e1s1_codon) <- c("barcode","b1a","b1b","b2a","b2b","b3a","b3b","b4a","b4b")
e1s1_codon <- merge(e1s1_codon, PTEN_library_variant_map_codon, by = "barcode", all = FALSE)
e1s1_codon[is.na(e1s1_codon)] <- 0

e1s1_codon <- e1s1_codon %>% group_by(value) %>% summarize(b1a = sum(b1a), b1b = sum(b1b), b2a = sum(b2a), b2b = sum(b2b), b3a = sum(b3a), b3b = sum(b3b), b4a = sum(b4a), b4b = sum(b4b), class = unique(class), variant = unique(variant))

e1s1_codon$b1 <- e1s1_codon$b1a + e1s1_codon$b1b; e1s1_codon$b2 <- e1s1_codon$b2a + e1s1_codon$b2b;e1s1_codon$b3 <- e1s1_codon$b3a + e1s1_codon$b3b; e1s1_codon$b4 <- e1s1_codon$b4a + e1s1_codon$b4b

e1s1_codon$b1 <- e1s1_codon$b1 / sum(e1s1_codon$b1, na.rm = TRUE)
e1s1_codon$b2 <- e1s1_codon$b2 / sum(e1s1_codon$b2, na.rm = TRUE)
e1s1_codon$b3 <- e1s1_codon$b3 / sum(e1s1_codon$b3, na.rm = TRUE)
e1s1_codon$b4 <- e1s1_codon$b4 / sum(e1s1_codon$b4, na.rm = TRUE)
e1s1_codon$mean_freq <- (e1s1_codon$b1 + e1s1_codon$b2 + e1s1_codon$b3 + e1s1_codon$b4) / 4

frequency_filter <- 1e-5 * 10^(1/4)
e1s1_codon <- subset(e1s1_codon, mean_freq > 1e-5 * 10^(1/4))
e1s1_codon <- subset(e1s1_codon, mean_freq != 0)
e1s1_codon$weighted_ave <- (e1s1_codon$b1 * 0 + e1s1_codon$b2 * (1/3) + e1s1_codon$b3 * (2/3) + e1s1_codon$b4) /
  rowSums(e1s1_codon[,c("b1","b2","b3","b4")])

write.csv(file = "output_datatables/e1s1_codon_weighted_ave.csv", e1s1_codon, row.names = FALSE, quote = FALSE)
```

``` r
e1s2_codon <- merge(e1s2_1a, e1s2_1b, by = "X", all = TRUE)
e1s2_codon <- merge(e1s2_codon, e1s2_2a, by = "X", all = TRUE)
e1s2_codon <- merge(e1s2_codon, e1s2_2b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s2_codon, e1s2_2b, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y' are duplicated in the result

``` r
e1s2_codon <- merge(e1s2_codon, e1s2_3a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s2_codon, e1s2_3a, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y' are duplicated in the result

``` r
e1s2_codon <- merge(e1s2_codon, e1s2_3b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s2_codon, e1s2_3b, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s2_codon <- merge(e1s2_codon, e1s2_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s2_codon, e1s2_4a, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s2_codon <- merge(e1s2_codon, e1s2_4b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s2_codon, e1s2_4b, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y', 'count.x', 'count.y', 'count.x', 'count.y' are
    ## duplicated in the result

``` r
colnames(e1s2_codon) <- c("barcode","b1a","b1b","b2a","b2b","b3a","b3b","b4a","b4b")
e1s2_codon <- merge(e1s2_codon, PTEN_library_variant_map_codon, by = "barcode", all = FALSE)
e1s2_codon[is.na(e1s2_codon)] <- 0

e1s2_codon <- e1s2_codon %>% group_by(value) %>% summarize(b1a = sum(b1a), b1b = sum(b1b), b2a = sum(b2a), b2b = sum(b2b), b3a = sum(b3a), b3b = sum(b3b), b4a = sum(b4a), b4b = sum(b4b), class = unique(class), variant = unique(variant))

e1s2_codon$b1 <- e1s2_codon$b1a + e1s2_codon$b1b; e1s2_codon$b2 <- e1s2_codon$b2a + e1s2_codon$b2b;e1s2_codon$b3 <- e1s2_codon$b3a + e1s2_codon$b3b; e1s2_codon$b4 <- e1s2_codon$b4a + e1s2_codon$b4b

e1s2_codon$b1 <- e1s2_codon$b1 / sum(e1s2_codon$b1, na.rm = TRUE)
e1s2_codon$b2 <- e1s2_codon$b2 / sum(e1s2_codon$b2, na.rm = TRUE)
e1s2_codon$b3 <- e1s2_codon$b3 / sum(e1s2_codon$b3, na.rm = TRUE)
e1s2_codon$b4 <- e1s2_codon$b4 / sum(e1s2_codon$b4, na.rm = TRUE)
e1s2_codon$mean_freq <- (e1s2_codon$b1 + e1s2_codon$b2 + e1s2_codon$b3 + e1s2_codon$b4) / 4
e1s2_codon <- subset(e1s2_codon, mean_freq > 1e-5 * 10^(1/4))
e1s2_codon <- subset(e1s2_codon, mean_freq != 0)
e1s2_codon$weighted_ave <- (e1s2_codon$b1 * 0 + e1s2_codon$b2 * (1/3) + e1s2_codon$b3 * (2/3) + e1s2_codon$b4) /
  rowSums(e1s2_codon[,c("b1","b2","b3","b4")])

write.csv(file = "Output_datatables/e1s2_codon_weighted_ave.csv", e1s2_codon, row.names = FALSE, quote = FALSE)
```

``` r
e1s3_codon <- merge(e1s3_1a, e1s3_1b, by = "X", all = TRUE)
e1s3_codon <- merge(e1s3_codon, e1s3_2a, by = "X", all = TRUE)
e1s3_codon <- merge(e1s3_codon, e1s3_2b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s3_codon, e1s3_2b, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y' are duplicated in the result

``` r
e1s3_codon <- merge(e1s3_codon, e1s3_3a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s3_codon, e1s3_3a, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y' are duplicated in the result

``` r
e1s3_codon <- merge(e1s3_codon, e1s3_3b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s3_codon, e1s3_3b, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s3_codon <- merge(e1s3_codon, e1s3_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s3_codon, e1s3_4a, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s3_codon <- merge(e1s3_codon, e1s3_4b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s3_codon, e1s3_4b, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y', 'count.x', 'count.y', 'count.x', 'count.y' are
    ## duplicated in the result

``` r
colnames(e1s3_codon) <- c("barcode","b1a","b1b","b2a","b2b","b3a","b3b","b4a","b4b")
e1s3_codon <- merge(e1s3_codon, PTEN_library_variant_map_codon, by = "barcode", all = FALSE)
e1s3_codon[is.na(e1s3_codon)] <- 0

e1s3_codon <- e1s3_codon %>% group_by(value) %>% summarize(b1a = sum(b1a), b1b = sum(b1b), b2a = sum(b2a), b2b = sum(b2b), b3a = sum(b3a), b3b = sum(b3b), b4a = sum(b4a), b4b = sum(b4b), class = unique(class), variant = unique(variant))

e1s3_codon$b1 <- e1s3_codon$b1a + e1s3_codon$b1b; e1s3_codon$b2 <- e1s3_codon$b2a + e1s3_codon$b2b;e1s3_codon$b3 <- e1s3_codon$b3a + e1s3_codon$b3b; e1s3_codon$b4 <- e1s3_codon$b4a + e1s3_codon$b4b

e1s3_codon$b1 <- e1s3_codon$b1 / sum(e1s3_codon$b1, na.rm = TRUE)
e1s3_codon$b2 <- e1s3_codon$b2 / sum(e1s3_codon$b2, na.rm = TRUE)
e1s3_codon$b3 <- e1s3_codon$b3 / sum(e1s3_codon$b3, na.rm = TRUE)
e1s3_codon$b4 <- e1s3_codon$b4 / sum(e1s3_codon$b4, na.rm = TRUE)
e1s3_codon$mean_freq <- (e1s3_codon$b1 + e1s3_codon$b2 + e1s3_codon$b3 + e1s3_codon$b4) / 4
e1s3_codon <- subset(e1s3_codon, mean_freq > 1e-5 * 10^(1/4))
e1s3_codon <- subset(e1s3_codon, mean_freq != 0)
e1s3_codon$weighted_ave <- (e1s3_codon$b1 * 0 + e1s3_codon$b2 * (1/3) + e1s3_codon$b3 * (2/3) + e1s3_codon$b4) /
  rowSums(e1s3_codon[,c("b1","b2","b3","b4")])

write.csv(file = "output_datatables/e1s3_codon_weighted_ave.csv", e1s3_codon, row.names = FALSE, quote = FALSE)
```

``` r
e1s4_codon <- merge(e1s4_1a, e1s4_1b, by = "X", all = TRUE)
e1s4_codon <- merge(e1s4_codon, e1s4_2a, by = "X", all = TRUE)
e1s4_codon <- merge(e1s4_codon, e1s4_2b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s4_codon, e1s4_2b, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y' are duplicated in the result

``` r
e1s4_codon <- merge(e1s4_codon, e1s4_3a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s4_codon, e1s4_3a, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y' are duplicated in the result

``` r
e1s4_codon <- merge(e1s4_codon, e1s4_3b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s4_codon, e1s4_3b, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s4_codon <- merge(e1s4_codon, e1s4_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s4_codon, e1s4_4a, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y', 'count.x', 'count.y' are duplicated in the result

``` r
e1s4_codon <- merge(e1s4_codon, e1s4_4b, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e1s4_codon, e1s4_4b, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y', 'count.x', 'count.y', 'count.x', 'count.y' are
    ## duplicated in the result

``` r
colnames(e1s4_codon) <- c("barcode","b1a","b1b","b2a","b2b","b3a","b3b","b4a","b4b")
e1s4_codon <- merge(e1s4_codon, PTEN_library_variant_map_codon, by = "barcode", all = FALSE)
e1s4_codon[is.na(e1s4_codon)] <- 0

e1s4_codon <- e1s4_codon %>% group_by(value) %>% summarize(b1a = sum(b1a), b1b = sum(b1b), b2a = sum(b2a), b2b = sum(b2b), b3a = sum(b3a), b3b = sum(b3b), b4a = sum(b4a), b4b = sum(b4b), class = unique(class), variant = unique(variant))

e1s4_codon$b1 <- e1s4_codon$b1a + e1s4_codon$b1b; e1s4_codon$b2 <- e1s4_codon$b2a + e1s4_codon$b2b;e1s4_codon$b3 <- e1s4_codon$b3a + e1s4_codon$b3b; e1s4_codon$b4 <- e1s4_codon$b4a + e1s4_codon$b4b

e1s4_codon$b1 <- e1s4_codon$b1 / sum(e1s4_codon$b1, na.rm = TRUE)
e1s4_codon$b2 <- e1s4_codon$b2 / sum(e1s4_codon$b2, na.rm = TRUE)
e1s4_codon$b3 <- e1s4_codon$b3 / sum(e1s4_codon$b3, na.rm = TRUE)
e1s4_codon$b4 <- e1s4_codon$b4 / sum(e1s4_codon$b4, na.rm = TRUE)
e1s4_codon$mean_freq <- (e1s4_codon$b1 + e1s4_codon$b2 + e1s4_codon$b3 + e1s4_codon$b4) / 4
e1s4_codon <- subset(e1s4_codon, mean_freq > 1e-5 * 10^(1/4))
e1s4_codon <- subset(e1s4_codon, mean_freq != 0)
e1s4_codon$weighted_ave <- (e1s4_codon$b1 * 0 + e1s4_codon$b2 * (1/3) + e1s4_codon$b3 * (2/3) + e1s4_codon$b4) /
  rowSums(e1s4_codon[,c("b1","b2","b3","b4")])

write.csv(file = "output_datatables/e1s4_codon_weighted_ave.csv", e1s4_codon, row.names = FALSE, quote = FALSE)
```

``` r
e3s1_codon <- merge(e3s1_1a, e3s1_2a, by = "X", all = TRUE)
e3s1_codon <- merge(e3s1_codon, e3s1_3a, by = "X", all = TRUE)
e3s1_codon <- merge(e3s1_codon, e3s1_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e3s1_codon, e3s1_4a, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y' are duplicated in the result

``` r
colnames(e3s1_codon) <- c("barcode","b1","b2","b3","b4")
e3s1_codon <- merge(e3s1_codon, PTEN_library_variant_map_codon, by = "barcode", all = FALSE)
e3s1_codon[is.na(e3s1_codon)] <- 0

e3s1_codon <- e3s1_codon %>% group_by(value) %>% summarize(b1 = sum(b1), b2 = sum(b2), b3 = sum(b3), b4 = sum(b4), class = unique(class), variant = unique(variant))

e3s1_codon$b1 <- e3s1_codon$b1 / sum(e3s1_codon$b1, na.rm = TRUE)
e3s1_codon$b2 <- e3s1_codon$b2 / sum(e3s1_codon$b2, na.rm = TRUE)
e3s1_codon$b3 <- e3s1_codon$b3 / sum(e3s1_codon$b3, na.rm = TRUE)
e3s1_codon$b4 <- e3s1_codon$b4 / sum(e3s1_codon$b4, na.rm = TRUE)
e3s1_codon$mean_freq <- (e3s1_codon$b1 + e3s1_codon$b2 + e3s1_codon$b3 + e3s1_codon$b4) / 4
e3s1_codon <- subset(e3s1_codon, mean_freq > 1e-5 * 10^(1/4))
e3s1_codon <- subset(e3s1_codon, mean_freq != 0)
e3s1_codon$weighted_ave <- (e3s1_codon$b1 * 0 + e3s1_codon$b2 * (1/3) + e3s1_codon$b3 * (2/3) + e3s1_codon$b4) /
  rowSums(e3s1_codon[,c("b1","b2","b3","b4")])

write.csv(file = "output_datatables/e3s1_codon_weighted_ave.csv", e3s1_codon, row.names = FALSE, quote = FALSE)
```

``` r
e3s2_codon <- merge(e3s2_1a, e3s2_2a, by = "X", all = TRUE)
e3s2_codon <- merge(e3s2_codon, e3s2_3a, by = "X", all = TRUE)
e3s2_codon <- merge(e3s2_codon, e3s2_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e3s2_codon, e3s2_4a, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y' are duplicated in the result

``` r
colnames(e3s2_codon) <- c("barcode","b1","b2","b3","b4")
e3s2_codon <- merge(e3s2_codon, PTEN_library_variant_map_codon, by = "barcode", all = FALSE)
e3s2_codon[is.na(e3s2_codon)] <- 0

e3s2_codon <- e3s2_codon %>% group_by(value) %>% summarize(b1 = sum(b1), b2 = sum(b2), b3 = sum(b3), b4 = sum(b4), class = unique(class), variant = unique(variant))

e3s2_codon$b1 <- e3s2_codon$b1 / sum(e3s2_codon$b1, na.rm = TRUE)
e3s2_codon$b2 <- e3s2_codon$b2 / sum(e3s2_codon$b2, na.rm = TRUE)
e3s2_codon$b3 <- e3s2_codon$b3 / sum(e3s2_codon$b3, na.rm = TRUE)
e3s2_codon$b4 <- e3s2_codon$b4 / sum(e3s2_codon$b4, na.rm = TRUE)
e3s2_codon$mean_freq <- (e3s2_codon$b1 + e3s2_codon$b2 + e3s2_codon$b3 + e3s2_codon$b4) / 4
e3s2_codon <- subset(e3s2_codon, mean_freq > 1e-5 * 10^(1/4))
e3s2_codon <- subset(e3s2_codon, mean_freq != 0)
e3s2_codon$weighted_ave <- (e3s2_codon$b1 * 0 + e3s2_codon$b2 * (1/3) + e3s2_codon$b3 * (2/3) + e3s2_codon$b4) /
  rowSums(e3s2_codon[,c("b1","b2","b3","b4")])

write.csv(file = "output_datatables/e3s2_codon_weighted_ave.csv", e3s2_codon, row.names = FALSE, quote = FALSE)
```

``` r
e3s3_codon <- merge(e3s3_1a, e3s3_2a, by = "X", all = TRUE)
e3s3_codon <- merge(e3s3_codon, e3s3_3a, by = "X", all = TRUE)
e3s3_codon <- merge(e3s3_codon, e3s3_4a, by = "X", all = TRUE)
```

    ## Warning in merge.data.frame(e3s3_codon, e3s3_4a, by = "X", all = TRUE): column
    ## names 'count.x', 'count.y' are duplicated in the result

``` r
colnames(e3s3_codon) <- c("barcode","b1","b2","b3","b4")
e3s3_codon <- merge(e3s3_codon, PTEN_library_variant_map_codon, by = "barcode", all = FALSE)
e3s3_codon[is.na(e3s3_codon)] <- 0

e3s3_codon <- e3s3_codon %>% group_by(value) %>% summarize(b1 = sum(b1), b2 = sum(b2), b3 = sum(b3), b4 = sum(b4), class = unique(class), variant = unique(variant))

e3s3_codon$b1 <- e3s3_codon$b1 / sum(e3s3_codon$b1, na.rm = TRUE)
e3s3_codon$b2 <- e3s3_codon$b2 / sum(e3s3_codon$b2, na.rm = TRUE)
e3s3_codon$b3 <- e3s3_codon$b3 / sum(e3s3_codon$b3, na.rm = TRUE)
e3s3_codon$b4 <- e3s3_codon$b4 / sum(e3s3_codon$b4, na.rm = TRUE)
e3s3_codon$mean_freq <- (e3s3_codon$b1 + e3s3_codon$b2 + e3s3_codon$b3 + e3s3_codon$b4) / 4
e3s3_codon <- subset(e3s3_codon, mean_freq > 1e-5 * 10^(1/4))
e3s3_codon <- subset(e3s3_codon, mean_freq != 0)
e3s3_codon$weighted_ave <- (e3s3_codon$b1 * 0 + e3s3_codon$b2 * (1/3) + e3s3_codon$b3 * (2/3) + e3s3_codon$b4) /
  rowSums(e3s3_codon[,c("b1","b2","b3","b4")])

write.csv(file = "output_datatables/e3s3_codon_weighted_ave.csv", e3s3_codon, row.names = FALSE, quote = FALSE)
```

``` r
#e1s1_codon <- read.csv(file = "output_datatables/e1s1_codon_weighted_ave.csv", header = T, stringsAsFactors = F)
#e1s2_codon <- read.csv(file = "output_datatables/e1s2_codon_weighted_ave.csv", header = T, stringsAsFactors = F)
#e1s3_codon <- read.csv(file = "output_datatables/e1s3_codon_weighted_ave.csv", header = T, stringsAsFactors = F)
#e1s4_codon <- read.csv(file = "output_datatables/e1s4_codon_weighted_ave.csv", header = T, stringsAsFactors = F)
#e3s1_codon <- read.csv(file = "output_datatables/e3s1_codon_weighted_ave.csv", header = T, stringsAsFactors = F)
#e3s2_codon <- read.csv(file = "output_datatables/e3s2_codon_weighted_ave.csv", header = T, stringsAsFactors = F)
#e3s3_codon <- read.csv(file = "output_datatables/e3s3_codon_weighted_ave.csv", header = T, stringsAsFactors = F)

e1s1_codon$position <- as.numeric(gsub("[A-Z]", "", e1s1_codon$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e1s1_codon$score1 <- (e1s1_codon$weighted_ave - median(subset(e1s1_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e1s1_codon, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e1s1_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))

e1s2_codon$position <- as.numeric(gsub("[A-Z]", "", e1s2_codon$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e1s2_codon$score2 <- (e1s2_codon$weighted_ave - median(subset(e1s2_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e1s2_codon, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e1s2_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))

e1s3_codon$position <- as.numeric(gsub("[A-Z]", "", e1s3_codon$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e1s3_codon$score3 <- (e1s3_codon$weighted_ave - median(subset(e1s3_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e1s3_codon, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e1s3_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))

e1s4_codon$position <- as.numeric(gsub("[A-Z]", "", e1s4_codon$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e1s4_codon$score4 <- (e1s4_codon$weighted_ave - median(subset(e1s4_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e1s4_codon, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e1s4_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))

e3s1_codon$position <- as.numeric(gsub("[A-Z]", "", e3s1_codon$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e3s1_codon$score5 <- (e3s1_codon$weighted_ave - median(subset(e3s1_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e3s1_codon, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e3s1_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))

e3s2_codon$position <- as.numeric(gsub("[A-Z]", "", e3s2_codon$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e3s2_codon$score6 <- (e3s2_codon$weighted_ave - median(subset(e3s2_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e3s2_codon, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e3s2_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))

e3s3_codon$position <- as.numeric(gsub("[A-Z]", "", e3s3_codon$variant))
```

    ## Warning: NAs introduced by coercion

``` r
e3s3_codon$score7 <- (e3s3_codon$weighted_ave - median(subset(e3s3_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE)) /
  (median(subset(e3s3_codon, class == "wt")$weighted_ave, na.rm = TRUE) - median(subset(e3s3_codon, position > 50 & position < 350 & class == "nonsense")$weighted_ave, na.rm = TRUE))
```

``` r
replicates_codon <- merge(e1s1_codon[,c("value","weighted_ave")], e1s2_codon[,c("value","weighted_ave")], by = "value", all = TRUE)
replicates_codon <- merge(replicates_codon, e1s3_codon[,c("value","weighted_ave")], by = "value", all = TRUE)
replicates_codon <- merge(replicates_codon, e1s4_codon[,c("value","weighted_ave")], by = "value", all = TRUE)
```

    ## Warning in merge.data.frame(replicates_codon, e1s4_codon[, c("value",
    ## "weighted_ave")], : column names 'weighted_ave.x', 'weighted_ave.y' are
    ## duplicated in the result

``` r
replicates_codon <- merge(replicates_codon, e3s1_codon[,c("value","weighted_ave")], by = "value", all = TRUE)
```

    ## Warning in merge.data.frame(replicates_codon, e3s1_codon[, c("value",
    ## "weighted_ave")], : column names 'weighted_ave.x', 'weighted_ave.y' are
    ## duplicated in the result

``` r
replicates_codon <- merge(replicates_codon, e3s2_codon[,c("value","weighted_ave")], by = "value", all = TRUE)
```

    ## Warning in merge.data.frame(replicates_codon, e3s2_codon[, c("value",
    ## "weighted_ave")], : column names 'weighted_ave.x', 'weighted_ave.y',
    ## 'weighted_ave.x', 'weighted_ave.y' are duplicated in the result

``` r
replicates_codon <- merge(replicates_codon, e3s3_codon[,c("value","weighted_ave")], by = "value", all = TRUE)
```

    ## Warning in merge.data.frame(replicates_codon, e3s3_codon[, c("value",
    ## "weighted_ave")], : column names 'weighted_ave.x', 'weighted_ave.y',
    ## 'weighted_ave.x', 'weighted_ave.y' are duplicated in the result

``` r
colnames(replicates_codon) <- c("value","e1s1","e1s2","e1s3","e1s4","e3s1","e3s2","e3s3")

replicates_codon$average <- rowMeans(replicates_codon[,c("e1s1","e1s2","e1s3","e1s4","e3s1","e3s2","e3s3")], na.rm = TRUE)
replicates_codon$count <- rowSums(cbind(!is.na(replicates_codon$e1s1),!is.na(replicates_codon$e1s2),!is.na(replicates_codon$e1s3),!is.na(replicates_codon$e1s4),!is.na(replicates_codon$e3s1),!is.na(replicates_codon$e3s2),!is.na(replicates_codon$e3s3)))

replicates_codon$sd <- rowMeans(cbind(abs(replicates_codon$average-replicates_codon$e1s1), abs(replicates_codon$average-replicates_codon$e1s2)
                                , abs(replicates_codon$average-replicates_codon$e1s3), abs(replicates_codon$average-replicates_codon$e1s4),
                                abs(replicates_codon$average-replicates_codon$e3s1),abs(replicates_codon$average-replicates_codon$e3s2),abs(replicates_codon$average-replicates_codon$e3s3)), na.rm = T)
```

``` r
## Need to extract individual variants from here

replicates_codon$aa_pos_1 <- 0
replicates_codon$aa_pos_2 <- 0
replicates_codon$aa_pos_3 <- 0
replicates_codon$aa_pos_4 <- 0
for(x in 1:nrow(replicates_codon)){
  replicates_codon$aa_pos_1[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(replicates_codon$value[x]), " \\(p"))[2],")"))[1]))
  replicates_codon$aa_pos_2[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(replicates_codon$value[x]), " \\(p"))[3],")"))[1]))
  replicates_codon$aa_pos_3[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(replicates_codon$value[x]), " \\(p"))[4],")"))[1]))
  replicates_codon$aa_pos_4[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(replicates_codon$value[x]), " \\(p"))[5],")"))[1]))
}

## Get all unique amino acid change positions from above
replicates_codon$change1 <- 0
replicates_codon$change2 <- 0
replicates_codon$change3 <- 0
for(x in 1:nrow(replicates_codon)){
  replicates_codon$change1[x] <- unique(c(replicates_codon$aa_pos_1[x], replicates_codon$aa_pos_2[x], replicates_codon$aa_pos_3[x], replicates_codon$aa_pos_4[x])[c(replicates_codon$aa_pos_1[x], replicates_codon$aa_pos_2[x], replicates_codon$aa_pos_3[x], replicates_codon$aa_pos_4[x]) != ""])[1]
  replicates_codon$change2[x] <- unique(c(replicates_codon$aa_pos_1[x], replicates_codon$aa_pos_2[x], replicates_codon$aa_pos_3[x], replicates_codon$aa_pos_4[x])[c(replicates_codon$aa_pos_1[x], replicates_codon$aa_pos_2[x], replicates_codon$aa_pos_3[x], replicates_codon$aa_pos_4[x]) != ""])[2]
  replicates_codon$change3[x] <- unique(c(replicates_codon$aa_pos_1[x], replicates_codon$aa_pos_2[x], replicates_codon$aa_pos_3[x], replicates_codon$aa_pos_4[x])[c(replicates_codon$aa_pos_1[x], replicates_codon$aa_pos_2[x], replicates_codon$aa_pos_3[x], replicates_codon$aa_pos_4[x]) != ""])[3]
  if(is.na(replicates_codon$change1[x] & !is.na(replicates_codon$change2[x]))){replicates_codon$change1[x] <- replicates_codon$change2[x]}
  if(is.na(replicates_codon$change2[x] & replicates_codon$change1[x] & !is.na(replicates_codon$change3[x]))){replicates_codon$change1[x] <- replicates_codon$change3[x]}
}

## Find the number of mutations for each variant
replicates_codon$mut_number <- 0
for(x in 1:nrow(replicates_codon)){
  replicates_codon$mut_number[x] <- 3-sum(is.na(replicates_codon[x,c("change1","change2","change3")]))
}

##
replicates_codon_singles <- subset(replicates_codon, mut_number == 1)
replicates_codon_wt <- subset(replicates_codon, value == "_wt" & mut_number == 0)
replicates_codon_syn <- subset(replicates_codon, !is.na(value) & value != "_wt" & mut_number == 0)

replicates_codon_singles$start_aa3 <- "NA"
replicates_codon_singles$end_aa3 <- "NA"

tempy <- subset(replicates_codon_singles, aa_pos_1 == 1)

for(x in 1:nrow(replicates_codon_syn)){
  replicates_codon_syn$position1[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(replicates_codon_syn$value[x]), split = "\\(p."))[1],3,
                                                              nchar(unlist(strsplit(x = as.character(replicates_codon_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  replicates_codon_syn$position2[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(replicates_codon_syn$value[x]), split = "\\(p."))[2],3,
                                                              nchar(unlist(strsplit(x = as.character(replicates_codon_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  replicates_codon_syn$position3[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(replicates_codon_syn$value[x]), split = "\\(p."))[3],3,
                                                              nchar(unlist(strsplit(x = as.character(replicates_codon_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  replicates_codon_syn$position4[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(replicates_codon_syn$value[x]), split = "\\(p."))[4],3,
                                                              nchar(unlist(strsplit(x = as.character(replicates_codon_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  replicates_codon_syn$change1[x] <- unique(c(replicates_codon_syn$position1[x], replicates_codon_syn$position2[x], replicates_codon_syn$position3[x], replicates_codon_syn$position4[x])[c(replicates_codon_syn$position1[x], replicates_codon_syn$position2[x], replicates_codon_syn$position3[x], replicates_codon_syn$position4[x]) != ""])[1]
  replicates_codon_syn$change2[x] <- unique(c(replicates_codon_syn$position1[x], replicates_codon_syn$position2[x], replicates_codon_syn$position3[x], replicates_codon_syn$position4[x])[c(replicates_codon_syn$position1[x], replicates_codon_syn$position2[x], replicates_codon_syn$position3[x], replicates_codon_syn$position4[x]) != ""])[2]
  replicates_codon_syn$change3[x] <- unique(c(replicates_codon_syn$position1[x], replicates_codon_syn$position2[x], replicates_codon_syn$position3[x], replicates_codon_syn$position4[x])[c(replicates_codon_syn$position1[x], replicates_codon_syn$position2[x], replicates_codon_syn$position3[x], replicates_codon_syn$position4[x]) != ""])[3]
  replicates_codon_syn$start[x] <- substr(pten_seq,replicates_codon_syn$change1[x],replicates_codon_syn$change1[x])
  replicates_codon_syn$end[x] <- replicates_codon_syn$start[x]
  replicates_codon_syn$variant[x] <- paste(replicates_codon_syn$start[x],replicates_codon_syn$change1[x],replicates_codon_syn$end[x],sep="")
}
```

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

``` r
for(x in 1:nrow(replicates_codon_singles)){
  replicates_codon_singles$start_aa3[x] <- as.character(gsub("[0-9]","",substr(unlist(strsplit(x = as.character(replicates_codon_singles$value[x]), split = "\\(p."))[2],1,4)))
  if(replicates_codon_singles$start_aa3[x] == "=), "){
    replicates_codon_singles$start_aa3[x] <- as.character(gsub("[0-9]","",substr(unlist(strsplit(x = as.character(replicates_codon_singles$value[x]), split = "\\(p."))[3],1,4)))
  }
  if(replicates_codon_singles$start_aa3[x] == "=), "){
    replicates_codon_singles$start_aa3[x] <- as.character(gsub("[0-9]","",substr(unlist(strsplit(x = as.character(replicates_codon_singles$value[x]), split = "\\(p."))[4],1,4)))
  }
  replicates_codon_singles$end_aa3[x] <- substr(unlist(strsplit(x = as.character(replicates_codon_singles$value[x]), split = ")"))[1],nchar(unlist(strsplit(x = as.character(replicates_codon_singles$value[x]), split = ")"))[1]) - 2,nchar(unlist(strsplit(x = as.character(replicates_codon_singles$value[x]), split = ")"))[1]))
  if(replicates_codon_singles$end_aa3[x] == "p.="){
    replicates_codon_singles$end_aa3[x] <- substr(unlist(strsplit(x = as.character(replicates_codon_singles$value[x]), split = ")"))[2],nchar(unlist(strsplit(x = as.character(replicates_codon_singles$value[x]), split = ")"))[2]) - 2,nchar(unlist(strsplit(x = as.character(replicates_codon_singles$value[x]), split = ")"))[2]))
  }
  if(replicates_codon_singles$end_aa3[x] == "p.="){
    replicates_codon_singles$end_aa3[x] <- substr(unlist(strsplit(x = as.character(replicates_codon_singles$value[x]), split = ")"))[3],nchar(unlist(strsplit(x = as.character(replicates_codon_singles$value[x]), split = ")"))[3]) - 2,nchar(unlist(strsplit(x = as.character(replicates_codon_singles$value[x]), split = ")"))[3]))
  }
}

for(x in 1:nrow(replicates_codon_singles)){
  replicates_codon_singles$position[x] <- replicates_codon_singles$aa_pos_1[x]
  if(replicates_codon_singles$position[x] == "" | is.na(replicates_codon_singles$position[x])){
    replicates_codon_singles$position[x] <- replicates_codon_singles$aa_pos_2[x]
  }
}

replicates_codon_singles$start <- "NA"
replicates_codon_singles$end <- "NA"
replicates_codon_singles$variant <- "NA"

for(x in 1:nrow(replicates_codon_singles)){
  replicates_codon_singles$start[x] <- to_single_notation(replicates_codon_singles$start_aa3[x])
  replicates_codon_singles$end[x] <- to_single_notation(replicates_codon_singles$end_aa3[x])
  replicates_codon_singles$variant[x] <- paste(replicates_codon_singles$start[x],replicates_codon_singles$position[x],replicates_codon_singles$end[x], sep="")
}

replicates_codon_nonsense <- subset(replicates_codon_singles, end == "X")
replicates_codon_missense <- subset(replicates_codon_singles, end != "X")

replicates_codon_syn$position <- replicates_codon_syn$position1
replicates_codon_wt$class <- "wt"
replicates_codon_wt$position <- 0
replicates_codon_wt$start <- "Z"
replicates_codon_wt$end <- "Z"
replicates_codon_syn$class <- "syn"
replicates_codon_nonsense$class <- "nonsense"
replicates_codon_missense$class <- "missense"
replicates_codon_wt$variant <- "wt"

replicates_codon_combined <- rbind(replicates_codon_wt[,c("value","variant","position","start","end","class","average","sd","count","e1s1","e1s2","e1s3","e1s4","e3s1","e3s2","e3s3")], replicates_codon_syn[,c("value","variant","position","start","end","class","average","sd","count","e1s1","e1s2","e1s3","e1s4","e3s1","e3s2","e3s3")],replicates_codon_nonsense[,c("value","variant","position","start","end","class","average","sd","count","e1s1","e1s2","e1s3","e1s4","e3s1","e3s2","e3s3")],replicates_codon_missense[,c("value","variant","position","start","end","class","average","sd","count","e1s1","e1s2","e1s3","e1s4","e3s1","e3s2","e3s3")])
```

``` r
replicates_codon_combined$start <- substr(gsub("[0-9]","",replicates_codon_combined$variant), 1,1)
replicates_codon_combined$end <- substr(gsub("[0-9]","",replicates_codon_combined$variant), 2,2)
replicates_codon_combined$position <- gsub("[^0-9]","",replicates_codon_combined$variant)

replicates_codon_combined[replicates_codon_combined$variant == "wt","start"] <- "Z"
replicates_codon_combined[replicates_codon_combined$variant == "wt","position"] <- "0"
replicates_codon_combined[replicates_codon_combined$variant == "wt","end"] <- "Z"

## Let's try to put in some abundance classifications here
replicates_codon_combined$se <- replicates_codon_combined$sd / sqrt(replicates_codon_combined$count)
replicates_codon_combined$lower_ci <- replicates_codon_combined$average - qnorm(0.975) * replicates_codon_combined$se
replicates_codon_combined$upper_ci <- replicates_codon_combined$average + qnorm(0.975) * replicates_codon_combined$se
replicates_codon_combined["average" == "NaN"] <- NA

synonymous_lowest_5percent <- quantile(subset(replicates_codon_combined, class == "syn")$average, 0.05, na.rm = TRUE)
synonymous_median <- quantile(subset(replicates_codon_combined, class == "syn")$average, 0.5, na.rm = TRUE)

replicates_codon_combined$position <- as.numeric(as.character(replicates_codon_combined$position))

replicates_codon_combined$score9 <- (replicates_codon_combined$e1s1 - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e1s1, na.rm = TRUE)) / 
  (median(subset(replicates_codon_combined, class == "wt")$e1s1, na.rm = TRUE) - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e1s1, na.rm = TRUE))

replicates_codon_combined$score10 <- (replicates_codon_combined$e1s2 - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e1s2, na.rm = TRUE)) / 
  (median(subset(replicates_codon_combined, class == "wt")$e1s2, na.rm = TRUE) - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e1s2, na.rm = TRUE))

replicates_codon_combined$score11 <- (replicates_codon_combined$e1s3 - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e1s3, na.rm = TRUE)) / 
  (median(subset(replicates_codon_combined, class == "wt")$e1s3, na.rm = TRUE) - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e1s3, na.rm = TRUE))

replicates_codon_combined$score12 <- (replicates_codon_combined$e1s4 - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e1s4, na.rm = TRUE)) / 
  (median(subset(replicates_codon_combined, class == "wt")$e1s4, na.rm = TRUE) - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e1s4, na.rm = TRUE))

replicates_codon_combined$score13 <- (replicates_codon_combined$e3s1 - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e3s1, na.rm = TRUE)) / 
  (median(subset(replicates_codon_combined, class == "wt")$e3s1, na.rm = TRUE) - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e3s1, na.rm = TRUE))

replicates_codon_combined$score14 <- (replicates_codon_combined$e3s2 - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e3s2, na.rm = TRUE)) / 
  (median(subset(replicates_codon_combined, class == "wt")$e3s2, na.rm = TRUE) - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e3s2, na.rm = TRUE))

replicates_codon_combined$score15 <- (replicates_codon_combined$e3s3 - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e3s3, na.rm = TRUE)) / 
  (median(subset(replicates_codon_combined, class == "wt")$e3s3, na.rm = TRUE) - median(subset(replicates_codon_combined, class == "nonsense" & position > 50 & position < 350)$e3s3, na.rm = TRUE))
```

# Set the universal filters for both the PTEN and TPMT data

``` r
#### Within the experiment, a variant had to be present a sum of this frequency across the four bins to be included in the analysis
frequency_filter <- 1e-5 * 10^(1/4)
frequency_filter <- 1*10^(-4.75)
#### Across the experiments, a variant had to be observed (passing the frequency filter) at least this number of experiments to be included in the analysis
experiment_filter <- 1
```

# Import and score PTEN experiments

``` r
pten_precursor <- read.table(file = "input_datatables/170530_PTEN_variants.m1", sep = "\t", header = TRUE, stringsAsFactors = FALSE)

pten_raw <- pten_precursor[,c("X","variant_SeqID_NT","variant_SeqID_AA","exp1_c_0", "exp1_c_1", "exp1_c_2", "exp1_c_3", "exp2_c_0", "exp2_c_1", "exp2_c_2", "exp2_c_3", "exp3_c_0", "exp3_c_1", "exp3_c_2", "exp3_c_3", "exp4_c_0", "exp4_c_1", "exp4_c_2", "exp4_c_3", "exp5_c_0", "exp5_c_1", "exp5_c_2", "exp5_c_3", "exp6_c_0", "exp6_c_1", "exp6_c_2", "exp6_c_3", "exp7_c_0", "exp7_c_1", "exp7_c_2", "exp7_c_3", "exp8_c_0", "exp8_c_1", "exp8_c_2", "exp8_c_3")]
colnames(pten_raw) <- c("value","variant_SeqID_NT","variant_SeqID_AA","exp1_bin1_count", "exp1_bin2_count", "exp1_bin3_count", "exp1_bin4_count", "exp2_bin1_count", "exp2_bin2_count", "exp2_bin3_count", "exp2_bin4_count", "exp3_bin1_count", "exp3_bin2_count", "exp3_bin3_count", "exp3_bin4_count", "exp4_bin1_count", "exp4_bin2_count", "exp4_bin3_count", "exp4_bin4_count", "exp5_bin1_count", "exp5_bin2_count", "exp5_bin3_count", "exp5_bin4_count", "exp6_bin1_count", "exp6_bin2_count", "exp6_bin3_count", "exp6_bin4_count", "exp7_bin1_count", "exp7_bin2_count", "exp7_bin3_count", "exp7_bin4_count", "exp8_bin1_count", "exp8_bin2_count", "exp8_bin3_count", "exp8_bin4_count")
pten_raw$position <- gsub("[^0-9]","",pten_raw$variant_SeqID_AA)
pten_raw$end <- gsub("[0-9-]","",pten_raw$variant_SeqID_AA)
pten_raw$end <- gsub("[*]","X",pten_raw$end)

pten_raw$codon <- gsub("[A-Z]","",pten_raw$variant_SeqID_NT)
for(x in 1:nrow(pten_raw)){
  pten_raw$codon[x] <- unlist(strsplit(unlist(strsplit(x = pten_raw$codon[x], split = c("-")))[1],","))[1]
}
pten_raw$codon_residue <- round((as.numeric(pten_raw$codon) + 1)/3)

pten_seq <- "MTAIIKEIVSRNKRRYQEDGFDLDLTYIYPNIIAMGFPAERLEGVYRNNIDDVVRFLDSKHKNHYKIYNLCAERHYDTAKFNCRVAQYPFEDHNPPQLELIKPFCEDLDQWLSEDDNHVAAIHCKAGKGRTGVMICAYLLHRGKFLKAQEALDFYGEVRTRDKKGVTIPSQRRYVYYYSYLLKNHLDYRPVALLFHKMMFETIPMFSGGTCNPQFVVCQLKVKIYSSNSGPTRREDKFMYFEFPQPLPVCGDIKVEFFHKQNKMLKKDKMFHFWVNTFFIPGPEETSEKVENGSLCDQEIDSICSIERADNDKEYLVLTLTKNDLDKANKDKANRYFSPNFKVKLYFTKTVEEPSNPEASSSTSVTPDVSDNEPDHYRYSDTTDSDPENEPFDEDQHTQITKV"

for(x in 1:nrow(pten_raw)){
  pten_raw$start <- substr(pten_seq,1,1)
}

pten_raw$class = "missense"
pten_raw[pten_raw$codon == 999,"class"] <- "wt"
pten_raw[pten_raw$end == "WTAA" & pten_raw$codon != 999,"class"] <- "synonymous"
pten_raw[pten_raw$end == "X","class"] <- "nonsense"

for(x in 1:nrow(pten_raw)){
  if(pten_raw$class[x] == "synonymous"){
    pten_raw$position[x] <- pten_raw$codon_residue[x]
    pten_raw$end[x] <- substr(pten_seq,pten_raw$position[x],pten_raw$position[x])
  }
}

pten_raw$start = "NA"
for(x in 1:nrow(pten_raw)){
  pten_raw$start[x] <- substr(pten_seq,pten_raw$position[x],pten_raw$position[x])
}

pten_raw[pten_raw$class == "wt","end"] <- "Z"
pten_raw[pten_raw$class == "wt","start"] <- "Z"
pten_raw[pten_raw$class == "wt","position"] <- "0"
pten_raw$variant <- paste(pten_raw$start,pten_raw$position,pten_raw$end,sep="")

## Add together all the bin frequencies to make a list of total variant frequency amount fo reach experiment
#library(plyr)

pten_raw[is.na(pten_raw)] <- 0
pten_raw3 <- pten_raw

## Now let's start getting frequencies
pten_raw3$exp1_bin1_freq <- pten_raw3$exp1_bin1_count / sum(pten_raw3$exp1_bin1_count, na.rm = TRUE)
pten_raw3$exp1_bin2_freq <- pten_raw3$exp1_bin2_count / sum(pten_raw3$exp1_bin2_count, na.rm = TRUE)
pten_raw3$exp1_bin3_freq <- pten_raw3$exp1_bin3_count / sum(pten_raw3$exp1_bin3_count, na.rm = TRUE)
pten_raw3$exp1_bin4_freq <- pten_raw3$exp1_bin4_count / sum(pten_raw3$exp1_bin4_count, na.rm = TRUE)
pten_raw3$exp2_bin1_freq <- pten_raw3$exp2_bin1_count / sum(pten_raw3$exp2_bin1_count, na.rm = TRUE)
pten_raw3$exp2_bin2_freq <- pten_raw3$exp2_bin2_count / sum(pten_raw3$exp2_bin2_count, na.rm = TRUE)
pten_raw3$exp2_bin3_freq <- pten_raw3$exp2_bin3_count / sum(pten_raw3$exp2_bin3_count, na.rm = TRUE)
pten_raw3$exp2_bin4_freq <- pten_raw3$exp2_bin4_count / sum(pten_raw3$exp2_bin4_count, na.rm = TRUE)
pten_raw3$exp3_bin1_freq <- pten_raw3$exp3_bin1_count / sum(pten_raw3$exp3_bin1_count, na.rm = TRUE)
pten_raw3$exp3_bin2_freq <- pten_raw3$exp3_bin2_count / sum(pten_raw3$exp3_bin2_count, na.rm = TRUE)
pten_raw3$exp3_bin3_freq <- pten_raw3$exp3_bin3_count / sum(pten_raw3$exp3_bin3_count, na.rm = TRUE)
pten_raw3$exp3_bin4_freq <- pten_raw3$exp3_bin4_count / sum(pten_raw3$exp3_bin4_count, na.rm = TRUE)
pten_raw3$exp4_bin1_freq <- pten_raw3$exp4_bin1_count / sum(pten_raw3$exp4_bin1_count, na.rm = TRUE)
pten_raw3$exp4_bin2_freq <- pten_raw3$exp4_bin2_count / sum(pten_raw3$exp4_bin2_count, na.rm = TRUE)
pten_raw3$exp4_bin3_freq <- pten_raw3$exp4_bin3_count / sum(pten_raw3$exp4_bin3_count, na.rm = TRUE)
pten_raw3$exp4_bin4_freq <- pten_raw3$exp4_bin4_count / sum(pten_raw3$exp4_bin4_count, na.rm = TRUE)
pten_raw3$exp5_bin1_freq <- pten_raw3$exp5_bin1_count / sum(pten_raw3$exp5_bin1_count, na.rm = TRUE)
pten_raw3$exp5_bin2_freq <- pten_raw3$exp5_bin2_count / sum(pten_raw3$exp5_bin2_count, na.rm = TRUE)
pten_raw3$exp5_bin3_freq <- pten_raw3$exp5_bin3_count / sum(pten_raw3$exp5_bin3_count, na.rm = TRUE)
pten_raw3$exp5_bin4_freq <- pten_raw3$exp5_bin4_count / sum(pten_raw3$exp5_bin4_count, na.rm = TRUE)
pten_raw3$exp6_bin1_freq <- pten_raw3$exp6_bin1_count / sum(pten_raw3$exp6_bin1_count, na.rm = TRUE)
pten_raw3$exp6_bin2_freq <- pten_raw3$exp6_bin2_count / sum(pten_raw3$exp6_bin2_count, na.rm = TRUE)
pten_raw3$exp6_bin3_freq <- pten_raw3$exp6_bin3_count / sum(pten_raw3$exp6_bin3_count, na.rm = TRUE)
pten_raw3$exp6_bin4_freq <- pten_raw3$exp6_bin4_count / sum(pten_raw3$exp6_bin4_count, na.rm = TRUE)
pten_raw3$exp7_bin1_freq <- pten_raw3$exp7_bin1_count / sum(pten_raw3$exp7_bin1_count, na.rm = TRUE)
pten_raw3$exp7_bin2_freq <- pten_raw3$exp7_bin2_count / sum(pten_raw3$exp7_bin2_count, na.rm = TRUE)
pten_raw3$exp7_bin3_freq <- pten_raw3$exp7_bin3_count / sum(pten_raw3$exp7_bin3_count, na.rm = TRUE)
pten_raw3$exp7_bin4_freq <- pten_raw3$exp7_bin4_count / sum(pten_raw3$exp7_bin4_count, na.rm = TRUE)
pten_raw3$exp8_bin1_freq <- pten_raw3$exp8_bin1_count / sum(pten_raw3$exp8_bin1_count, na.rm = TRUE)
pten_raw3$exp8_bin2_freq <- pten_raw3$exp8_bin2_count / sum(pten_raw3$exp8_bin2_count, na.rm = TRUE)
pten_raw3$exp8_bin3_freq <- pten_raw3$exp8_bin3_count / sum(pten_raw3$exp8_bin3_count, na.rm = TRUE)
pten_raw3$exp8_bin4_freq <- pten_raw3$exp8_bin4_count / sum(pten_raw3$exp8_bin4_count, na.rm = TRUE)

## Getting total counts and total freqs
pten_raw3$exp1_total_count <- rowSums(pten_raw3[,c("exp1_bin1_count", "exp1_bin2_count", "exp1_bin3_count", "exp1_bin4_count")], na.rm = TRUE)
pten_raw3$exp2_total_count <- rowSums(pten_raw3[,c("exp2_bin1_count", "exp2_bin2_count", "exp2_bin3_count", "exp2_bin4_count")], na.rm = TRUE)
pten_raw3$exp3_total_count <- rowSums(pten_raw3[,c("exp3_bin1_count", "exp3_bin2_count", "exp3_bin3_count", "exp3_bin4_count")], na.rm = TRUE)
pten_raw3$exp4_total_count <- rowSums(pten_raw3[,c("exp4_bin1_count", "exp4_bin2_count", "exp4_bin3_count", "exp4_bin4_count")], na.rm = TRUE)
pten_raw3$exp5_total_count <- rowSums(pten_raw3[,c("exp5_bin1_count", "exp5_bin2_count", "exp5_bin3_count", "exp5_bin4_count")], na.rm = TRUE)
pten_raw3$exp6_total_count <- rowSums(pten_raw3[,c("exp6_bin1_count", "exp6_bin2_count", "exp6_bin3_count", "exp6_bin4_count")], na.rm = TRUE)
pten_raw3$exp7_total_count <- rowSums(pten_raw3[,c("exp7_bin1_count", "exp7_bin2_count", "exp7_bin3_count", "exp7_bin4_count")], na.rm = TRUE)
pten_raw3$exp8_total_count <- rowSums(pten_raw3[,c("exp8_bin1_count", "exp8_bin2_count", "exp8_bin3_count", "exp8_bin4_count")], na.rm = TRUE)

pten_raw3$exp1_total_freq <- rowSums(pten_raw3[,c("exp1_bin1_freq", "exp1_bin2_freq", "exp1_bin3_freq", "exp1_bin4_freq")], na.rm = TRUE)
pten_raw3$exp2_total_freq <- rowSums(pten_raw3[,c("exp2_bin1_freq", "exp2_bin2_freq", "exp2_bin3_freq", "exp2_bin4_freq")], na.rm = TRUE)
pten_raw3$exp3_total_freq <- rowSums(pten_raw3[,c("exp3_bin1_freq", "exp3_bin2_freq", "exp3_bin3_freq", "exp3_bin4_freq")], na.rm = TRUE)
pten_raw3$exp4_total_freq <- rowSums(pten_raw3[,c("exp4_bin1_freq", "exp4_bin2_freq", "exp4_bin3_freq", "exp4_bin4_freq")], na.rm = TRUE)
pten_raw3$exp5_total_freq <- rowSums(pten_raw3[,c("exp5_bin1_freq", "exp5_bin2_freq", "exp5_bin3_freq", "exp5_bin4_freq")], na.rm = TRUE)
pten_raw3$exp6_total_freq <- rowSums(pten_raw3[,c("exp6_bin1_freq", "exp6_bin2_freq", "exp6_bin3_freq", "exp6_bin4_freq")], na.rm = TRUE)
pten_raw3$exp7_total_freq <- rowSums(pten_raw3[,c("exp7_bin1_freq", "exp7_bin2_freq", "exp7_bin3_freq", "exp7_bin4_freq")], na.rm = TRUE)
pten_raw3$exp8_total_freq <- rowSums(pten_raw3[,c("exp8_bin1_freq", "exp8_bin2_freq", "exp8_bin3_freq", "exp8_bin4_freq")], na.rm = TRUE)

pten_raw3$exp1_total_countfreq <- (pten_raw3$exp1_bin1_count + pten_raw3$exp1_bin2_count + pten_raw3$exp1_bin3_count + pten_raw3$exp1_bin4_count)/(sum(pten_raw3$exp1_bin1_count, na.rm = TRUE) + sum(pten_raw3$exp1_bin2_count, na.rm = TRUE) + sum(pten_raw3$exp1_bin3_count, na.rm = TRUE) + sum(pten_raw3$exp1_bin4_count, na.rm = TRUE))
pten_raw3$exp2_total_countfreq <- (pten_raw3$exp2_bin1_count + pten_raw3$exp2_bin2_count + pten_raw3$exp2_bin3_count + pten_raw3$exp2_bin4_count)/(sum(pten_raw3$exp2_bin1_count, na.rm = TRUE) + sum(pten_raw3$exp2_bin2_count, na.rm = TRUE) + sum(pten_raw3$exp2_bin3_count, na.rm = TRUE) + sum(pten_raw3$exp2_bin4_count, na.rm = TRUE))
pten_raw3$exp3_total_countfreq <- (pten_raw3$exp3_bin1_count + pten_raw3$exp3_bin2_count + pten_raw3$exp3_bin3_count + pten_raw3$exp3_bin4_count)/(sum(pten_raw3$exp3_bin1_count, na.rm = TRUE) + sum(pten_raw3$exp3_bin2_count, na.rm = TRUE) + sum(pten_raw3$exp3_bin3_count, na.rm = TRUE) + sum(pten_raw3$exp3_bin4_count, na.rm = TRUE))
pten_raw3$exp4_total_countfreq <- (pten_raw3$exp4_bin1_count + pten_raw3$exp4_bin2_count + pten_raw3$exp4_bin3_count + pten_raw3$exp4_bin4_count)/(sum(pten_raw3$exp4_bin1_count, na.rm = TRUE) + sum(pten_raw3$exp4_bin2_count, na.rm = TRUE) + sum(pten_raw3$exp4_bin3_count, na.rm = TRUE) + sum(pten_raw3$exp4_bin4_count, na.rm = TRUE))
pten_raw3$exp5_total_countfreq <- (pten_raw3$exp5_bin1_count + pten_raw3$exp5_bin2_count + pten_raw3$exp5_bin3_count + pten_raw3$exp5_bin4_count)/(sum(pten_raw3$exp5_bin1_count, na.rm = TRUE) + sum(pten_raw3$exp5_bin2_count, na.rm = TRUE) + sum(pten_raw3$exp5_bin3_count, na.rm = TRUE) + sum(pten_raw3$exp5_bin4_count, na.rm = TRUE))
pten_raw3$exp6_total_countfreq <- (pten_raw3$exp6_bin1_count + pten_raw3$exp6_bin2_count + pten_raw3$exp6_bin3_count + pten_raw3$exp6_bin4_count)/(sum(pten_raw3$exp6_bin1_count, na.rm = TRUE) + sum(pten_raw3$exp6_bin2_count, na.rm = TRUE) + sum(pten_raw3$exp6_bin3_count, na.rm = TRUE) + sum(pten_raw3$exp6_bin4_count, na.rm = TRUE))
pten_raw3$exp7_total_countfreq <- (pten_raw3$exp7_bin1_count + pten_raw3$exp7_bin2_count + pten_raw3$exp7_bin3_count + pten_raw3$exp7_bin4_count)/(sum(pten_raw3$exp7_bin1_count, na.rm = TRUE) + sum(pten_raw3$exp7_bin2_count, na.rm = TRUE) + sum(pten_raw3$exp7_bin3_count, na.rm = TRUE) + sum(pten_raw3$exp7_bin4_count, na.rm = TRUE))
pten_raw3$exp8_total_countfreq <- (pten_raw3$exp8_bin1_count + pten_raw3$exp8_bin2_count + pten_raw3$exp8_bin3_count + pten_raw3$exp8_bin4_count)/(sum(pten_raw3$exp8_bin1_count, na.rm = TRUE) + sum(pten_raw3$exp8_bin2_count, na.rm = TRUE) + sum(pten_raw3$exp8_bin3_count, na.rm = TRUE) + sum(pten_raw3$exp8_bin4_count, na.rm = TRUE))
```

``` r
pten_raw3$exp1_w_ave <- NA
pten_raw3$exp2_w_ave <- NA
pten_raw3$exp3_w_ave <- NA
pten_raw3$exp4_w_ave <- NA
pten_raw3$exp5_w_ave <- NA
pten_raw3$exp6_w_ave <- NA
pten_raw3$exp7_w_ave <- NA
pten_raw3$exp8_w_ave <- NA
pten_raw3$median_w_ave <- NA

#frequency_filter = 1

for(x in 1:nrow(pten_raw3)){
  if(pten_raw3$exp1_total_countfreq[x] >= frequency_filter){pten_raw3$exp1_w_ave[x] <- (pten_raw3$exp1_bin1_freq[x] * 0.25 + pten_raw3$exp1_bin2_freq[x] * 0.5 + pten_raw3$exp1_bin3_freq[x] * 0.75 + pten_raw3$exp1_bin4_freq[x])/pten_raw3$exp1_total_freq[x]}
  if(pten_raw3$exp2_total_countfreq[x] >= frequency_filter){pten_raw3$exp2_w_ave[x] <- (pten_raw3$exp2_bin1_freq[x] * 0.25 + pten_raw3$exp2_bin2_freq[x] * 0.5 + pten_raw3$exp2_bin3_freq[x] * 0.75 + pten_raw3$exp2_bin4_freq[x])/pten_raw3$exp2_total_freq[x]}
  if(pten_raw3$exp3_total_countfreq[x] >= frequency_filter){pten_raw3$exp3_w_ave[x] <- (pten_raw3$exp3_bin1_freq[x] * 0.25 + pten_raw3$exp3_bin2_freq[x] * 0.5 + pten_raw3$exp3_bin3_freq[x] * 0.75 + pten_raw3$exp3_bin4_freq[x])/pten_raw3$exp3_total_freq[x]}
  if(pten_raw3$exp4_total_countfreq[x] >= frequency_filter){pten_raw3$exp4_w_ave[x] <- (pten_raw3$exp4_bin1_freq[x] * 0.25 + pten_raw3$exp4_bin2_freq[x] * 0.5 + pten_raw3$exp4_bin3_freq[x] * 0.75 + pten_raw3$exp4_bin4_freq[x])/pten_raw3$exp4_total_freq[x]}
  if(pten_raw3$exp5_total_countfreq[x] >= frequency_filter){pten_raw3$exp5_w_ave[x] <- (pten_raw3$exp5_bin1_freq[x] * 0.25 + pten_raw3$exp5_bin2_freq[x] * 0.5 + pten_raw3$exp5_bin3_freq[x] * 0.75 + pten_raw3$exp5_bin4_freq[x])/pten_raw3$exp5_total_freq[x]}
  if(pten_raw3$exp6_total_countfreq[x] >= frequency_filter){pten_raw3$exp6_w_ave[x] <- (pten_raw3$exp6_bin1_freq[x] * 0.25 + pten_raw3$exp6_bin2_freq[x] * 0.5 + pten_raw3$exp6_bin3_freq[x] * 0.75 + pten_raw3$exp6_bin4_freq[x])/pten_raw3$exp6_total_freq[x]}
  if(pten_raw3$exp7_total_countfreq[x] >= frequency_filter){pten_raw3$exp7_w_ave[x] <- (pten_raw3$exp7_bin1_freq[x] * 0.25 + pten_raw3$exp7_bin2_freq[x] * 0.5 + pten_raw3$exp7_bin3_freq[x] * 0.75 + pten_raw3$exp7_bin4_freq[x])/pten_raw3$exp7_total_freq[x]}
  if(pten_raw3$exp8_total_countfreq[x] >= frequency_filter){pten_raw3$exp8_w_ave[x] <- (pten_raw3$exp8_bin1_freq[x] * 0.25 + pten_raw3$exp8_bin2_freq[x] * 0.5 + pten_raw3$exp8_bin3_freq[x] * 0.75 + pten_raw3$exp8_bin4_freq[x])/pten_raw3$exp8_total_freq[x]}
  pten_raw3$median_w_ave[x] <- median(as.numeric(pten_raw3[x,c("exp1_w_ave","exp2_w_ave","exp3_w_ave","exp4_w_ave","exp5_w_ave","exp6_w_ave","exp7_w_ave","exp8_w_ave")]), na.rm = TRUE)
}

pten_raw3[is.na(pten_raw3)] <- 0

pten_raw3$position <- as.numeric(gsub("[^0-9]", "", pten_raw3$variant))
pten_raw3[pten_raw3$variant == "Z0Z", "position"] <- 0
pten_raw3$start <- substr(pten_raw3$variant,1,1)
pten_raw3$end <- substr(pten_raw3$variant,nchar(pten_raw3$variant),nchar(pten_raw3$variant))

pten_raw3$class <- NA
for(x in 1:nrow(pten_raw3)){
  if(pten_raw3[x,"end"] == "X"){pten_raw3[x,"class"] <- "nonsense"}
  if(pten_raw3[x,"end"] != "X" & pten_raw3[x,"end"] != "Z"){pten_raw3[x,"class"] <- "missense"}
  if(pten_raw3[x,"start"] == pten_raw3[x,"end"]){pten_raw3[x,"class"] <- "synonymous"}
  if(pten_raw3[x,"variant"] == "Z0Z"){pten_raw3[x,"class"] <- "wt"}
}

pten_raw3[pten_raw3 == 0] <- NA
pten_raw3[pten_raw3 == "NaN"] <- NA

### Adding an expt filter here
pten_raw3$expts <- rowSums(!is.na(pten_raw3[,c("exp1_w_ave","exp2_w_ave","exp3_w_ave","exp4_w_ave","exp5_w_ave","exp6_w_ave","exp7_w_ave","exp8_w_ave")]))
pten_raw3 <- subset(pten_raw3, expts >= experiment_filter)

pten_raw3$score1 <- (pten_raw3$exp1_w_ave - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp1_w_ave, na.rm = TRUE)) / 
  (median(subset(pten_raw3, class == "wt")$exp1_w_ave, na.rm = TRUE) - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp1_w_ave, na.rm = TRUE))

pten_raw3$score2 <- (pten_raw3$exp2_w_ave - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp2_w_ave, na.rm = TRUE)) / 
  (median(subset(pten_raw3, class == "wt")$exp2_w_ave, na.rm = TRUE) - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp2_w_ave, na.rm = TRUE))

pten_raw3$score3 <- (pten_raw3$exp3_w_ave - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp3_w_ave, na.rm = TRUE)) / 
  (median(subset(pten_raw3, class == "wt")$exp3_w_ave, na.rm = TRUE) - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp3_w_ave, na.rm = TRUE))

pten_raw3$score4 <- (pten_raw3$exp4_w_ave - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp4_w_ave, na.rm = TRUE)) / 
  (median(subset(pten_raw3, class == "wt")$exp4_w_ave, na.rm = TRUE) - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp4_w_ave, na.rm = TRUE))

pten_raw3$score5 <- (pten_raw3$exp5_w_ave - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp5_w_ave, na.rm = TRUE)) / 
  (median(subset(pten_raw3, class == "wt")$exp5_w_ave, na.rm = TRUE) - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp5_w_ave, na.rm = TRUE))

pten_raw3$score6 <- (pten_raw3$exp6_w_ave - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp6_w_ave, na.rm = TRUE)) / 
  (median(subset(pten_raw3, class == "wt")$exp6_w_ave, na.rm = TRUE) - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp6_w_ave, na.rm = TRUE))

pten_raw3$score7 <- (pten_raw3$exp7_w_ave - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp7_w_ave, na.rm = TRUE)) / 
  (median(subset(pten_raw3, class == "wt")$exp7_w_ave, na.rm = TRUE) - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp7_w_ave, na.rm = TRUE))

pten_raw3$score8 <- (pten_raw3$exp8_w_ave - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp8_w_ave, na.rm = TRUE)) / 
  (median(subset(pten_raw3, class == "wt")$exp8_w_ave, na.rm = TRUE) - median(subset(pten_raw3, class == "nonsense" & position > 50 & position < 350)$exp8_w_ave, na.rm = TRUE))

pten_raw3$score <- rowMeans(pten_raw3[,c("score1","score2","score3","score4","score5","score6","score7","score8")], na.rm = TRUE)

pten_raw3$sd <- apply(pten_raw3[,c("score1","score2","score3","score4","score5","score6","score7","score8")],1,sd, na.rm = TRUE)

pten_raw3$se <- pten_raw3$sd / sqrt(pten_raw3$expts)
pten_raw3[pten_raw3 == "NaN"] <- NA

synonymous_lowest_5percent <- quantile(subset(pten_raw3, class == "synonymous")$score, 0.05, na.rm = TRUE)
synonymous_median <- quantile(subset(pten_raw3, class == "synonymous")$score, 0.5, na.rm = TRUE)
synonymous_highest <- quantile(subset(pten_raw3, class == "synonymous")$score, 0.95, na.rm = TRUE)

pten_variants_orig <- pten_raw3[,c("value","variant","class","position","score","sd","expts","score1","score2","score3","score4","score5","score6","score7","score8")]
```

``` r
codon_level_fully_combined <- merge(pten_variants_orig[,c("value","score","score1","score2","score3","score4","score5","score6","score7","score8")], replicates_codon_combined[,c("value","variant","class","position","count","score9","score10","score11","score12","score13","score14","score15")], by = "value", all = T)

codon_level_fully_combined$aa_pos_1 <- 0
codon_level_fully_combined$aa_pos_2 <- 0
codon_level_fully_combined$aa_pos_3 <- 0
codon_level_fully_combined$aa_pos_4 <- 0
for(x in 1:nrow(codon_level_fully_combined)){
  codon_level_fully_combined$aa_pos_1[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(codon_level_fully_combined$value[x]), " \\(p"))[2],")"))[1]))
  codon_level_fully_combined$aa_pos_2[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(codon_level_fully_combined$value[x]), " \\(p"))[3],")"))[1]))
  codon_level_fully_combined$aa_pos_3[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(codon_level_fully_combined$value[x]), " \\(p"))[4],")"))[1]))
  codon_level_fully_combined$aa_pos_4[x] <- as.double(gsub("[^0-9]","",unlist(strsplit(unlist(strsplit(as.character(codon_level_fully_combined$value[x]), " \\(p"))[5],")"))[1]))
}

## Get all unique amino acid change positions from above
codon_level_fully_combined$change1 <- 0
codon_level_fully_combined$change2 <- 0
codon_level_fully_combined$change3 <- 0
for(x in 1:nrow(codon_level_fully_combined)){
  codon_level_fully_combined$change1[x] <- unique(c(codon_level_fully_combined$aa_pos_1[x], codon_level_fully_combined$aa_pos_2[x], codon_level_fully_combined$aa_pos_3[x], codon_level_fully_combined$aa_pos_4[x])[c(codon_level_fully_combined$aa_pos_1[x], codon_level_fully_combined$aa_pos_2[x], codon_level_fully_combined$aa_pos_3[x], codon_level_fully_combined$aa_pos_4[x]) != ""])[1]
  codon_level_fully_combined$change2[x] <- unique(c(codon_level_fully_combined$aa_pos_1[x], codon_level_fully_combined$aa_pos_2[x], codon_level_fully_combined$aa_pos_3[x], codon_level_fully_combined$aa_pos_4[x])[c(codon_level_fully_combined$aa_pos_1[x], codon_level_fully_combined$aa_pos_2[x], codon_level_fully_combined$aa_pos_3[x], codon_level_fully_combined$aa_pos_4[x]) != ""])[2]
  codon_level_fully_combined$change3[x] <- unique(c(codon_level_fully_combined$aa_pos_1[x], codon_level_fully_combined$aa_pos_2[x], codon_level_fully_combined$aa_pos_3[x], codon_level_fully_combined$aa_pos_4[x])[c(codon_level_fully_combined$aa_pos_1[x], codon_level_fully_combined$aa_pos_2[x], codon_level_fully_combined$aa_pos_3[x], codon_level_fully_combined$aa_pos_4[x]) != ""])[3]
  if(is.na(codon_level_fully_combined$change1[x] & !is.na(codon_level_fully_combined$change2[x]))){codon_level_fully_combined$change1[x] <- codon_level_fully_combined$change2[x]}
  if(is.na(codon_level_fully_combined$change2[x] & codon_level_fully_combined$change1[x] & !is.na(codon_level_fully_combined$change3[x]))){codon_level_fully_combined$change1[x] <- codon_level_fully_combined$change3[x]}
}

## Find the number of mutations for each variant
codon_level_fully_combined$mut_number <- 0
for(x in 1:nrow(codon_level_fully_combined)){
  codon_level_fully_combined$mut_number[x] <- 3-sum(is.na(codon_level_fully_combined[x,c("change1","change2","change3")]))
}

##
codon_level_fully_combined_singles <- subset(codon_level_fully_combined, mut_number == 1)
codon_level_fully_combined_wt <- subset(codon_level_fully_combined, value == "_wt" & mut_number == 0)
codon_level_fully_combined_syn <- subset(codon_level_fully_combined, !is.na(value) & value != "_wt" & mut_number == 0)

codon_level_fully_combined_singles$start_aa3 <- "NA"
codon_level_fully_combined_singles$end_aa3 <- "NA"

tempy <- subset(codon_level_fully_combined_singles, aa_pos_1 == 1)

for(x in 1:nrow(codon_level_fully_combined_syn)){
  codon_level_fully_combined_syn$position1[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(codon_level_fully_combined_syn$value[x]), split = "\\(p."))[1],3,
                                                              nchar(unlist(strsplit(x = as.character(codon_level_fully_combined_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  codon_level_fully_combined_syn$position2[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(codon_level_fully_combined_syn$value[x]), split = "\\(p."))[2],3,
                                                              nchar(unlist(strsplit(x = as.character(codon_level_fully_combined_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  codon_level_fully_combined_syn$position3[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(codon_level_fully_combined_syn$value[x]), split = "\\(p."))[3],3,
                                                              nchar(unlist(strsplit(x = as.character(codon_level_fully_combined_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  codon_level_fully_combined_syn$position4[x] <- as.integer(as.numeric(substr(unlist(strsplit(x = as.character(codon_level_fully_combined_syn$value[x]), split = "\\(p."))[4],3,
                                                              nchar(unlist(strsplit(x = as.character(codon_level_fully_combined_syn$value[x]), split = "\\(p."))[1])-4))/3 - 1/6) + 1
  codon_level_fully_combined_syn$change1[x] <- unique(c(codon_level_fully_combined_syn$position1[x], codon_level_fully_combined_syn$position2[x], codon_level_fully_combined_syn$position3[x], codon_level_fully_combined_syn$position4[x])[c(codon_level_fully_combined_syn$position1[x], codon_level_fully_combined_syn$position2[x], codon_level_fully_combined_syn$position3[x], codon_level_fully_combined_syn$position4[x]) != ""])[1]
  codon_level_fully_combined_syn$change2[x] <- unique(c(codon_level_fully_combined_syn$position1[x], codon_level_fully_combined_syn$position2[x], codon_level_fully_combined_syn$position3[x], codon_level_fully_combined_syn$position4[x])[c(codon_level_fully_combined_syn$position1[x], codon_level_fully_combined_syn$position2[x], codon_level_fully_combined_syn$position3[x], codon_level_fully_combined_syn$position4[x]) != ""])[2]
  codon_level_fully_combined_syn$change3[x] <- unique(c(codon_level_fully_combined_syn$position1[x], codon_level_fully_combined_syn$position2[x], codon_level_fully_combined_syn$position3[x], codon_level_fully_combined_syn$position4[x])[c(codon_level_fully_combined_syn$position1[x], codon_level_fully_combined_syn$position2[x], codon_level_fully_combined_syn$position3[x], codon_level_fully_combined_syn$position4[x]) != ""])[3]
  codon_level_fully_combined_syn$start[x] <- substr(pten_seq,codon_level_fully_combined_syn$change1[x],codon_level_fully_combined_syn$change1[x])
  codon_level_fully_combined_syn$end[x] <- codon_level_fully_combined_syn$start[x]
  codon_level_fully_combined_syn$variant[x] <- paste(codon_level_fully_combined_syn$start[x],codon_level_fully_combined_syn$change1[x],codon_level_fully_combined_syn$end[x],sep="")
}
```

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

    ## Warning: NAs introduced by coercion

``` r
for(x in 1:nrow(codon_level_fully_combined_singles)){
  codon_level_fully_combined_singles$start_aa3[x] <- as.character(gsub("[0-9]","",substr(unlist(strsplit(x = as.character(codon_level_fully_combined_singles$value[x]), split = "\\(p."))[2],1,4)))
  if(codon_level_fully_combined_singles$start_aa3[x] == "=), "){
    codon_level_fully_combined_singles$start_aa3[x] <- as.character(gsub("[0-9]","",substr(unlist(strsplit(x = as.character(codon_level_fully_combined_singles$value[x]), split = "\\(p."))[3],1,4)))
  }
  if(codon_level_fully_combined_singles$start_aa3[x] == "=), "){
    codon_level_fully_combined_singles$start_aa3[x] <- as.character(gsub("[0-9]","",substr(unlist(strsplit(x = as.character(codon_level_fully_combined_singles$value[x]), split = "\\(p."))[4],1,4)))
  }
  codon_level_fully_combined_singles$end_aa3[x] <- substr(unlist(strsplit(x = as.character(codon_level_fully_combined_singles$value[x]), split = ")"))[1],nchar(unlist(strsplit(x = as.character(codon_level_fully_combined_singles$value[x]), split = ")"))[1]) - 2,nchar(unlist(strsplit(x = as.character(codon_level_fully_combined_singles$value[x]), split = ")"))[1]))
  if(codon_level_fully_combined_singles$end_aa3[x] == "p.="){
    codon_level_fully_combined_singles$end_aa3[x] <- substr(unlist(strsplit(x = as.character(codon_level_fully_combined_singles$value[x]), split = ")"))[2],nchar(unlist(strsplit(x = as.character(codon_level_fully_combined_singles$value[x]), split = ")"))[2]) - 2,nchar(unlist(strsplit(x = as.character(codon_level_fully_combined_singles$value[x]), split = ")"))[2]))
  }
  if(codon_level_fully_combined_singles$end_aa3[x] == "p.="){
    codon_level_fully_combined_singles$end_aa3[x] <- substr(unlist(strsplit(x = as.character(codon_level_fully_combined_singles$value[x]), split = ")"))[3],nchar(unlist(strsplit(x = as.character(codon_level_fully_combined_singles$value[x]), split = ")"))[3]) - 2,nchar(unlist(strsplit(x = as.character(codon_level_fully_combined_singles$value[x]), split = ")"))[3]))
  }
}

for(x in 1:nrow(codon_level_fully_combined_singles)){
  codon_level_fully_combined_singles$position[x] <- codon_level_fully_combined_singles$aa_pos_1[x]
  if(codon_level_fully_combined_singles$position[x] == "" | is.na(codon_level_fully_combined_singles$position[x])){
    codon_level_fully_combined_singles$position[x] <- codon_level_fully_combined_singles$aa_pos_2[x]
  }
}

codon_level_fully_combined_singles$start <- "NA"
codon_level_fully_combined_singles$end <- "NA"
codon_level_fully_combined_singles$variant <- "NA"

for(x in 1:nrow(codon_level_fully_combined_singles)){
  codon_level_fully_combined_singles$start[x] <- to_single_notation(codon_level_fully_combined_singles$start_aa3[x])
  codon_level_fully_combined_singles$end[x] <- to_single_notation(codon_level_fully_combined_singles$end_aa3[x])
  codon_level_fully_combined_singles$variant[x] <- paste(codon_level_fully_combined_singles$start[x],codon_level_fully_combined_singles$position[x],codon_level_fully_combined_singles$end[x], sep="")
}

codon_level_fully_combined_nonsense <- subset(codon_level_fully_combined_singles, end == "X")
codon_level_fully_combined_missense <- subset(codon_level_fully_combined_singles, end != "X")

codon_level_fully_combined_syn$position <- codon_level_fully_combined_syn$position1
codon_level_fully_combined_wt$class <- "wt"
codon_level_fully_combined_wt$position <- 0
codon_level_fully_combined_wt$start <- "Z"
codon_level_fully_combined_wt$end <- "Z"
codon_level_fully_combined_syn$class <- "syn"
codon_level_fully_combined_nonsense$class <- "nonsense"
codon_level_fully_combined_missense$class <- "missense"
codon_level_fully_combined_wt$variant <- "wt"

PTEN_library_variant_codon_level_fully_combined <- rbind(codon_level_fully_combined_wt[,c("value","variant","score","score1","score2","score3","score4","score5","score6","score7","score8","score9","score10","score11","score12","score13","score14","score15")], codon_level_fully_combined_syn[,c("value","variant","score","score1","score2","score3","score4","score5","score6","score7","score8","score9","score10","score11","score12","score13","score14","score15")],codon_level_fully_combined_nonsense[,c("value","variant","score","score1","score2","score3","score4","score5","score6","score7","score8","score9","score10","score11","score12","score13","score14","score15")],codon_level_fully_combined_missense[,c("value","variant","score","score1","score2","score3","score4","score5","score6","score7","score8","score9","score10","score11","score12","score13","score14","score15")])
```

``` r
codon_score_collapsed_orig <- PTEN_library_variant_codon_level_fully_combined %>% filter(!is.na(score)) %>% mutate(count = 1)
codon_score_collapsed_orig2 <- codon_score_collapsed_orig %>% group_by(variant) %>% summarize(mean_orig = mean(score, na.rm = T), sd_orig = sd(score, na.rm = T), count_orig = sum(count))
  
PTEN_library_variant_codon_level_fully_combined$combined_score <- rowMeans(PTEN_library_variant_codon_level_fully_combined[,c("score1","score2","score3","score4","score5","score6","score7","score8","score9","score10","score11","score12","score13","score14","score15")], na.rm = TRUE)

codon_score_collapsed_combined <- PTEN_library_variant_codon_level_fully_combined %>% mutate(count = 1) %>% group_by(variant) %>% summarize(mean_combined = mean(combined_score, na.rm = T), sd_combined = sd(combined_score, na.rm = T), count_combined = sum(count))


codon_score_collapsed_orig_multiple <- codon_score_collapsed_orig2 %>% filter(count_orig >= 2)
codon_score_collapsed_orig_multiple$cv_orig <- codon_score_collapsed_orig_multiple$sd_orig / codon_score_collapsed_orig_multiple$mean_orig

codon_score_collapsed_combined_multiple <- codon_score_collapsed_combined %>% filter(count_combined >= 2)
codon_score_collapsed_combined_multiple$cv_combined <- codon_score_collapsed_combined_multiple$sd_combined / codon_score_collapsed_combined_multiple$mean_combined

multiple_codon_analysis <- merge(codon_score_collapsed_orig_multiple, codon_score_collapsed_combined_multiple, by = "variant", all = T)

Coefficient_of_variation_plot_codon <- 
ggplot() + theme_bw() + 
  scale_x_continuous(limits = c(-0.25,1.8)) +
  geom_histogram(data = multiple_codon_analysis, aes(x = cv_orig), fill = "blue", alpha = 0.5, color = "blue", binwidth = 0.05) +
  geom_histogram(data = multiple_codon_analysis, aes(x = cv_combined), fill = "red", alpha = 0.5, color = "red", binwidth = 0.05) +
  geom_vline(xintercept = 0.5, linetype = 2, alpha = 0.4) + geom_vline(xintercept = 0, linetype = 2, alpha = 0.4) +
  ylab("Number of variants") + xlab("Coefficient of variation")
Coefficient_of_variation_plot_codon
```

    ## Warning: Removed 447 rows containing non-finite values (stat_bin).

    ## Warning: Removed 27 rows containing non-finite values (stat_bin).

    ## Warning: Removed 2 rows containing missing values (geom_bar).

    ## Warning: Removed 2 rows containing missing values (geom_bar).

![](PTEN_composite_analysis_files/figure-gfm/unnamed-chunk-1-1.png)<!-- -->

``` r
ggsave(file = "Plots/Coefficient_of_variation_plot_codon.pdf", Coefficient_of_variation_plot_codon, height = 40, width = 60, units = "mm")
```

    ## Warning: Removed 447 rows containing non-finite values (stat_bin).

    ## Warning: Removed 27 rows containing non-finite values (stat_bin).

    ## Warning: Removed 2 rows containing missing values (geom_bar).

    ## Warning: Removed 2 rows containing missing values (geom_bar).

``` r
paste("There were", nrow(codon_score_collapsed_orig_multiple), "variants in the original data set that were scored based on the mean of two or more unique codon scores")
```

    ## [1] "There were 1500 variants in the original data set that were scored based on the mean of two or more unique codon scores"

``` r
paste("The median coefficient of variation in the mean scores of amino acid variants encoded by two or more codons is", round(median(codon_score_collapsed_orig_multiple$cv_orig),2))
```

    ## [1] "The median coefficient of variation in the mean scores of amino acid variants encoded by two or more codons is 0.15"

``` r
paste("There were", nrow(codon_score_collapsed_combined_multiple), "variants in the composite data set that were scored based on the mean of two or more unique codon scores")
```

    ## [1] "There were 1935 variants in the composite data set that were scored based on the mean of two or more unique codon scores"

``` r
paste("The median coefficient of variation in the mean scores of amino acid variants encoded by two or more codons is", round(median(codon_score_collapsed_combined_multiple$cv_combined),2))
```

    ## [1] "The median coefficient of variation in the mean scores of amino acid variants encoded by two or more codons is 0.16"
