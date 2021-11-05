library(ggplot2)
library(ggpmisc)
data <- read.table('input3.txt',header=T)
RACE <- data$RACE
GCGC <- data$GCGC
#p <- ggplot(data,aes(x=RACE,y=GCGC))
#p + geom_point()+geom_smooth(method='lm',color='black',formula= y ~ x )+ geom_point()

#lm_eqn <- function(df){
#  m <- lm(y ~ x, df);
#  eq <- substitute(italic(y) == a + b %.% italic(x)*","~~italic(r)^2~"="~r2, 
#                   list(a = format(unname(coef(m)[1]), digits = 2),
#                        b = format(unname(coef(m)[2]), digits = 2),
#                        r2 = format(summary(m)$r.squared, digits = 3)))
#  as.character(as.expression(eq));
#}

#p1 <- p + 
#  geom_text(x = 25, y = 300, 
#            label = lm_eqn(data), parse = TRUE)
#p1
my.formula = y ~ x
ggplot(data = data, aes(x = RACE, y = GCGC)) +
geom_smooth(method = "lm", 
              se=FALSE, color="black", 
              formula = my.formula) +
  stat_poly_eq(formula = my.formula, 
               aes(label = paste(..eq.label.., 
                                 ..rr.label.., 
                                 sep = "~~~")), 
               parse = TRUE) +         
  geom_point(size=2,
             alpha=0.7,
             color="#fe654c")+
  coord_cartesian(ylim = c(0,1),
                  xlim = c(0,1))+
  scale_y_continuous(breaks = c(0,0.5,1))+
  scale_x_continuous(breaks = c(0,0.5,1))+
  theme_bw()+
  geom_smooth(method = "lm",
              color="#558ebd",
              fill="lightgray",
              alpha=.7,
              size=0.5,se=T,
              formula = y~x)+
  theme(panel.grid = element_blank(),axis.text=element_text(size=18),axis.title=element_text(size=20,face="bold"))
