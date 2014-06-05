tabla <- read.csv("/home/nicolas/QB9-git/QB9/resources/dataframesinesp.csv", header = TRUE, sep = ",", quote = "\"")
tablalinda<- read.csv("/home/nicolas/QB9-git/QB9/resources/dataframesinesp.csv", header = TRUE, sep = ",", quote = "\"")
plot.new()


y~x
linea <- lm(tabla$Decay ~ tabla$solo)
plot(x=tabla$solo,y=tabla$Decay, main = "Tabla", pch = 21, bg = "red")
abline(linea$coefficients)


linea$coefficients
linea$residuals
linea$

line(linea$)

pairs(tabla, main = "Tabla")

panel.cor <- function(x, y, digits=2, prefix="", cex.cor)
{
  usr <- par("usr"); on.exit(par(usr))
  par(usr = c(0, 1, 0, 1))
  r = (cor(x, y))
  txt <- format(c(r, 0.123456789), digits=digits)[1]
  txt <- paste(prefix, txt, sep="")
  if(missing(cex.cor)) cex <- 0.8/strwidth(txt)
  text(0.5, 0.5, txt, cex = cex * abs(r))
}
tabla1<- data.frame(tabla$total,tabla$solo,tabla$acomp,tabla$Nucleo,tabla$Redox)
tabla2 <- data.frame()
pairs(tabla1, lower.panel=panel.smooth, upper.panel=panel.cor)

summary(linea)
