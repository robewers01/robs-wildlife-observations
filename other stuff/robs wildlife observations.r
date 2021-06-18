

clean.names <- function(x){
	names(x)[c(6,7,11,12,17:20)] <- c("Species","Taxa","lat","long","Latin","Common","Date","Status")
	return(x)
	}


	
	taxa.list <- function(obs_data, latin = TRUE){
		#obs_data = dataframe of observations to extract information from
		#latin = analyse species within families?
		
		if(latin == TRUE){
			#families
			family.list <- sort(unique(obs_data$Species))
			family.date <- obs_data[, c('Species', 'Date')]
			#genera and species
			fam.sub <- obs_data[which(obs_data$Latin != ""), ]
			species.list <- sort(unique(fam.sub$Latin))
			species.date <- fam.sub[, c('Latin', 'Date')]
			names(species.date) <- c('Species', 'Date')
			}else{
				species.list <- sort(unique(obs_data$Species))
				species.date <- obs_data[, c('Species', 'Date')]
				family.list <- NA
				family.date <- NA
				}
		
		return(list(family.list = family.list, family.date = family.date,
			species.list = species.list, species.date = species.date))
		}


	species.accum <- function(species_date){
		#species_date = dataframe containing species ID and date of observations
		
		species_date$Date <- as.Date(species_date$Date, format="%d/%m/%y")
		dates <- sort(unique(species_date$Date))
		
		#Quantify cumulative number of species
		accum.data <- matrix(NA, nrow = length(dates), ncol = 2)
		for(i in 1:length(dates)){
			data.sub <- species_date[species_date$Date <= dates[i], ]
			accum.data[i,1] <- dates[i]
			accum.data[i,2] <- length(unique(data.sub$Species))	#Total species
			}
		
		return(accum.data)
		}


summary.obs <- function(obs_form, target = 'global', search.radius = 1000, 
	accum.curve = TRUE){
	#target = lat and long coordinates of location being considered
		#If target = 'global', all records are considered regardless of location
	#search.radius = distance (m) from target within which records are considered
	#accum.curve = plot rate of taxon accumulation
	
	#Read in libraries
	require(RANN)
	require(vegan)

	#Update field names
	obs_form <- clean.names(obs_form)

	#Geographic search limits
	if(length(target)==1){
		local.obs <- obs_form
		}else{
			if(is.na(search.radius)){
				local.obs <- obs_form
				}else{
					#Identify points within radius
					sightings <- nn2(obs_form[,11:12], target, k=nrow(obs_form), searchtype="radius", radius=search.radius)
					#Which observations fall within target radius
					observations <- sort(sightings$nn.idx[sightings$nn.idx != 0])
					#Subset local observations
					local.obs <- obs_form[observations,]
					}
			}
	
	#Get lists of species and/or families per taxonomicl group
	birds <- taxa.list(local.obs[local.obs$Taxa == 'Bird', ], latin = FALSE)
	herps <- taxa.list(local.obs[local.obs$Taxa == 'Reptile or amphibian', ], latin = FALSE)
	mammals <- taxa.list(local.obs[local.obs$Taxa == 'Mammal', ], latin = FALSE)
	plants <- taxa.list(local.obs[local.obs$Taxa == 'Plant', ], latin = TRUE)
	inverts <- taxa.list(local.obs[local.obs$Taxa == 'Invertebrate', ], latin = TRUE)
	
	birds.spp <- birds$species.list
	herps.spp <- herps$species.list
	mamm.spp <- mammals$species.list
	plants.fam <- plants$family.list
	plants.spp <- plants$species.list
	inverts.fam <- inverts$family.list
	inverts.spp <- inverts$species.list
	
	total.spp <- length(birds.spp) + length(herps.spp) + length(mamm.spp) +
		length(plants.spp) + length(inverts.spp)
	total.fam <- length(plants.fam) + length(inverts.fam)

	print(paste("You have identified",total.spp,"species and",total.fam,"families across all taxa", sep = " "))
	print(paste(length(birds.spp), "species of bird", sep = " "))
	print(paste(length(herps.spp), "species of reptiles and amphibians", sep = " "))
	print(paste(length(mamm.spp), "species of mammal", sep = " "))
	print(paste(length(plants.spp),"species of plant within",length(plants.fam), "families", sep = " "))
	print(paste(length(inverts.spp),"species of invertebrate within",length(inverts.fam), "families", sep = " "))

	
	#Species accumulation curves
	if(accum.curve == TRUE){
		#Total number of species
		species.date <- rbind(birds$species.date, mammals$species.date, herps$species.date, plants$species.date, inverts$species.date)
		species.date$Date <- as.Date(species.date$Date, format="%d/%m/%y")
		species.date <- species.date[order(species.date$Date),]
		
		total.accum <- species.accum(species.date)
		
			#Plot cumulative number of species
			plot(total.accum[,1], total.accum[,2], pch = 19, type = 'b',
				ylim = c(0, total.spp), ylab = "Number of taxa",
				xaxt = 'n',
				xlim = c(min(species.date$Date), max(species.date$Date)), xlab = "Date"
				)
				axis(1, species.date$Date, format(species.date$Date, "%b %y"))
		
		#Birds
		birds.accum <- species.accum(birds$species.date)
		lines(birds.accum[,1], birds.accum[,2], col = 2, lwd = 2)
		#Plants
		plants.accum <- species.accum(plants$species.date)
		lines(plants.accum[,1], plants.accum[,2], col = 3, lwd = 2)
		#Mammals
		mamms.accum <- species.accum(mammals$species.date)
		lines(mamms.accum[,1], mamms.accum[,2], col = 4, lwd = 2)
		#Herps
		herps.accum <- species.accum(herps$species.date)
		lines(herps.accum[,1], herps.accum[,2], col = 6, lwd = 2)
		#Inverts
		inverts.accum <- species.accum(inverts$species.date)
		lines(inverts.accum[,1], inverts.accum[,2], col = 8, lwd = 2)
		
		#Plant familiess
		plantfams.accum <- species.accum(plants$family.date)
		lines(plantfams.accum[,1], plantfams.accum[,2], col = 'darkgreen', lwd = 3, lty=2)
		#Invert familiess
		invertfams.accum <- species.accum(inverts$family.date)
		lines(invertfams.accum[,1], invertfams.accum[,2], col = 'darkgrey', lwd = 3, lty=2)
	
		legend('topleft', legend = c('Total species','Bird species','Plant species','Mammal species','Herpetofauna species','Invertebrate species',
			'Plant families','Invertebrate families'), 
			lwd = c(rep(2,6), rep(3,2)), cex = 1, , bg = "white",
			col=c(1:4,6,8,'darkgreen','darkgrey'),
			lty=c(rep(1,6), rep(2,2))
			)
		}
	
	#Info to return
	return(list(
		birds = birds.spp,
		herps = herps.spp,
		mammals = mamm.spp,
		plants.spp = plants.spp,
		plants.fam = plants.fam,
		inverts.spp = inverts.spp,
		inverts.fam = inverts.fam
		))

	}




#Read in data
obs_form <- read.csv("C:\\Users\\robew\\Dropbox (Personal)\\work\\data sets\\robs wildlife observations\\form-1__wildlife.csv")
	#Change obvious synonyms
	obs_form$X2_Species[obs_form$X2_Species == 'Town pigeon'] <- 'Rock dove'


#Global summary
global.sum <- summary.obs(obs_form)
	global.sum$plants.fam
	global.sum$inverts.fam
	global.sum$birds

#Target coordinates
sitio <- data.frame(lat=c(7402738), long=c(207634))
sitio.sum <- summary.obs(obs_form, target = sitio,  search.radius = 2000)
	sitio.sum$birds
	sitio.sum$mammals
	
home <- data.frame(lat=c(5698851), long=c(651564))
home.sum <- summary.obs(obs_form, target = home,  search.radius = 2000)
	home.sum$birds
















