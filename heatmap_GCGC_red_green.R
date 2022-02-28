library(pheatmap)
data <- read.table('input.list2.deal.addtitle',header=T,row.names= 1)
anno <- read.table('annotation.list',header=T,row.names= 1)
ann_colors <- list(CLASS = c(class1 = "#D95F02", class0 = "##1874CD"))
pdf('GCGC_heatmap.pdf',width=12,height=8)
exprTable_t <- as.data.frame(t(data))
mat <- dist(exprTable_t)
hclust_mat <- hclust(mat)
index <- seq(1,60, by = 1)
hclust_mat$order <- index
#col_cluster <- hclust_mat$labels
#manual_order = c("GA14P","GA16P","GA18P","GA24P","GA50P","GA54P","GA55P","GA58P","GA87P","GA92P","RG785NM1","RG790NM1","RG796NM1","RG869NM1","RG870NM1","RG872NM1","RG881NM1","RG883NM1","RG895NM1","RG897NM1","RG898NM1","RH421NM1","RH902NM1","RH903NM1","RJ219NX2","RK508NX2","RL221NX1","RL268NX1","RL701NX1","RL717NX1","RG788NM1","RG792NM1","RG887NM1","RG889NM1","RG899NM1","RG900NM1","RH291NM1","RH459NX1","RH883NM1","RH885NX1","RJ137NX2","RJ218NX2","RK314NX2","RK337NX2","RL182NX1","RL185NX1","RL235NX1","RL239NX1","RL338NX1","RL340NX1","RL353NX1","RL354NX1","RL356NX1","RL357NX1","RL359NX1","RL360NX1","RL367NX1","RL412NX1","RL417NX1","RG797NM1")
#dend = reorder(as.dendrogram(hclust_mat), wts=order(match(manual_order, rownames(data))), agglo.FUN = min)
#dend = reorder(as.dendrogram(hclust_mat), wts=order(match(manual_order, rownames(data))))
#col_cluster <- as.hclust(dend)
#col_cluster
pheatmap(data, cluster_cols = hclust_mat,
         color = colorRampPalette(c("##1874CD", "yellow", "#D95F02"))(60), 
         show_rownames=T,show_colnames=T,
         display_numbers = FALSE,
         treeheight_row = 0, treeheight_col = 0,
         fontsize = 9,
         cellwidth = 10, cellheight = 10,
         legend_labels = c('0','0.2','0.4','0.6','0.8','1'),
         annotation_col = anno, annotation_colors = ann_colors
         )
dev.off()
