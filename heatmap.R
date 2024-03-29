library(pheatmap)
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]
anno_list <- args[2]
out_file <- args[3]
data <- read.table(input_file,header=T,row.names= 1)
anno <- read.table(anno_list,header=T,row.names= 1)
ann_colors <- list(CLASS = c(class1 = "#D95F02", class0 = "#6495ED"))
pdf(out_file,width=12,height=8)
exprTable_t <- as.data.frame(t(data))
mat <- dist(exprTable_t)
hclust_mat <- hclust(mat)
index <- seq(1,60, by = 1)
hclust_mat$order <- index
pheatmap(data, cluster_cols = hclust_mat,
         color = colorRampPalette(c("#6495ED", "#FFDAB9", "#D95F02"))(60), 
         show_rownames=T,show_colnames=T,
         display_numbers = FALSE,
         treeheight_row = 0, treeheight_col = 0,
         fontsize = 9,
         cellwidth = 10, cellheight = 10,
         legend_labels = c('0','0.2','0.4','0.6','0.8','1'),
         annotation_col = anno, annotation_colors = ann_colors
         )
dev.off()
