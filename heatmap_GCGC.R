library(pheatmap)
data <- read.table('input.list2.deal.addtitle',header=T,row.names= 1)
anno <- read.table('annotation.list',header=T,row.names= 1)
ann_colors <- list(CLASS = c(class1 = "#D95F02", class0 = "#6495ED"))
pdf('GCGC_heatmap.pdf',width=12,height=8)
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
