args <- commandArgs(trailingOnly = TRUE)

df <- read.table(args[1], header=T, sep = "\t",as.is=TRUE)
rep_num <- as.numeric(args[3])

M_mean <- df$Obs_Ratio
m_mean <- df$Batch_Ratio

std   <- df$exp_std
pvals <- c()
abs_d <- c()

for(i in 1:length(M_mean)){
	if(m_mean[i] <  M_mean[i]){
		M <- M_mean[i]
		m <- m_mean[i]
		p <- pnorm( m_mean[i] , M_mean[i] , sqrt(std[i]*std[i]/rep_num) )
	} else {
		M <- m_mean[i]
        m <- M_mean[i]
        p <- 1 - pnorm( m_mean[i] , M_mean[i] , sqrt(std[i]*std[i]/rep_num) )
    }
	pvals <- c(pvals, 2*p ) 
	abs_d <- c(abs_d, abs(M-m))
}

#FDR <- p.adjust(pvals, "BH")

out_df <- data.frame( df$SiteID , df$Mean_Coverage, M_mean, m_mean, df$exp_std, abs_d, pvals, df$gene, df$region, df$alu, df$batch )
colnames(out_df) <- c("SiteID" , "Mean_Coverage",  "Obs_Ratio", "Batch_Ratio", "exp_std","ABS" ,"pvals", "gene", "region", "alu", "batch")
write.table( out_df , args[2] , quote = F,row.names =F ,sep="\t")

print("Script finished, DONE")


