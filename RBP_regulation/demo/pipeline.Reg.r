library(ggplot2)
args <- commandArgs(trailingOnly = TRUE)

ExportPlot <- function(gplot, filename, width = 4, height = 3.5) {
        # Export plot in PDF and EPS.
        # Notice that A4: width=11.69, height=8.27
        pdf(file = paste(filename, '.pdf', sep = ""), width = width, height = height)
        print(gplot)
        dev.off()
        postscript(file = paste(filename, '.eps', sep = ""), width = width, height = height)
        print(gplot)
        dev.off()
}

df <- read.table(args[1], header=T, sep = "\t", as.is=TRUE)
colnames(df) <- c("SiteID", "Mean_Coverage", "Var_Ratio", "Mean_Ratio")

MC <- max(df$Mean_Coverage)
mC <- min(df$Mean_Coverage)

testC <- c()

testf <- read.table(args[2], header=T, sep = "\t",as.is=TRUE)
colnames(testf) <- c("SiteID", "Obs_Ratio", "Mean_Coverage", "Batch_Ratio", "gene", "region", "alu", "batch")

for (i in 1:length(testf$Mean_Coverage)){
  if(testf$Mean_Coverage[i] > MC){
	testC <- c(testC, MC)
	print(testf$Mean_Coverage[i])
    print(MC)
  }else if (testf$Mean_Coverage[i] < mC) {
	testC <- c(testC, mC)
	print(testf$Mean_Coverage[i])
    print(mC)
  }else{
	testC <- c(testC, testf$Mean_Coverage[i])
  }
}

myloess <- loess(df$Var_Ratio ~ df$Mean_Coverage, data = df)
predX   <- predict(myloess, df$Mean_Coverage, se = TRUE)
predY   <- predict(myloess, testC, se = TRUE)
RawVarY <- predY$fit + 2*predY$s
expVarY <- c()

for (i in 1:length(RawVarY)){
  if(RawVarY[i] < 0.001){
	expVarY <- c(expVarY, 0.001)
  } else{
	expVarY <- c(expVarY, RawVarY[i])
  }
}

std <- sqrt(expVarY)

# Write down file
Res <- data.frame(testf$SiteID, testf$Obs_Ratio, testf$Mean_Coverage, testf$Batch_Ratio, expVarY, std, testf$gene, testf$region, testf$alu, testf$batch)
colnames(Res) <- c("SiteID", "Obs_Ratio", "Mean_Coverage", "Batch_Ratio", "exp_Var", "exp_std", "gene", "region", "alu", "batch")
write.table(Res, args[3] , sep="\t", quote=F, col.names = T, row.names = F)


RawVarX  <- predX$fit + 2*predX$s
expVarX  <- c()

for (i in 1:length(RawVarX)){
  if(RawVarX[i] < 0.001){
        expVarX <- c(expVarX, 0.001)
  } else{
        expVarX <- c(expVarX, RawVarX[i])
  }
}



# Make plot
p1 <- ggplot(df, aes(x = df$Mean_Coverage, y = df$Var_Ratio ))+
      geom_point(shape = 21)+
      geom_line(aes(y=predX$fit), colour="red")+
      geom_line(aes(y=expVarX), colour="blue")+
      labs(x = "Mean_Coverage", y="Var_Ratio")+
      theme(axis.text.x = element_text(size=8), 
    	axis.text.y  = element_text(size=8), 
    	axis.title   = element_text(size=10),
    	axis.line    = element_line(colour="black"), 
        plot.title   = element_text(size=8, face="bold"),
        legend.text  = element_text(size=10), 
    	legend.key   = element_rect(fill="white"),
        legend.title = element_text(size=10), #,face="bold"),
    	strip.text.x = element_text(size=10), 
        strip.background = element_rect(fill='white'),
        panel.grid.major = element_blank(), 
    	panel.grid.minor = element_blank(),
        panel.background = element_blank())

ExportPlot(p1, args[3])

print("Plot made and script finished, DONE")
