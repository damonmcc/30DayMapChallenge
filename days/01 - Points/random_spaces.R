# credit to https://github.com/BlakeRMills/30DayMapChallenge
library(readr)
library(geojsonio)
library(tidyverse)
library(sf)
library(showtext)
library(sysfonts)
library(cowplot)

# Configuration
# borough_name <- "Manhattan"
# borough_initials <- "MN"
borough_name <- "Brooklyn"
borough_initials <- "BK"

script_dir <- dirname(sys.frame(1)$ofile)
file_path <- paste(script_dir, "/01 Points - ", borough_name, " Random Spaces - ", Sys.time(), ".png", sep="")

# Data
pluto <- read_csv("data/pluto_21v4.csv")  # https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page
borMap <- geojson_sf("data/Borough Boundaries.geojson") # https://data.cityofnewyork.us/City-Government/Borough-Boundaries/tqmj-j8zm


# Format
point_size <- 0.15
point_alpha <- 0.4
showtext_auto()
font_add_google("Josefin Sans")
font1 <- "Josefin Sans"
labelx <- 0.71
labelfontsize <- 18


# Data Wrangling2

borMap <- borMap %>% filter(boro_name == borough_name)

pluto <- pluto %>% filter(borough == borough_initials, numfloors != 0)
# pluto <- pluto %>% mutate(BuildingType = case_when(grepl("J", bldgclass)==TRUE ~ "Theatre",
#                                                    bldgclass == "P7" ~ "Museum",
#                                                    bldgclass == "P8" ~ "Library",
#                                                    bldgclass == "Q0" ~ "Open Space",
#                                                    bldgclass == "Q1" ~ "Park",
#                                                    bldgclass == "Q2" ~ "Playground",
#                                                    bldgclass == "QG" ~ "Commuity Garden",
#                                                    TRUE ~ "Other")) %>%
#   filter(borough == borough_initials, BuildingType != "Other")


# Main Plot
p1 <- ggplot() + 
  geom_sf(data=borMap, aes(geometry=geometry), color="grey15", fill="grey35") +
  geom_point(data=pluto, aes(x=longitude, y=latitude, color=numfloors), alpha=point_alpha, size=point_size) +
  # scale_color_manual(values = c("#ffe287", "#ffb47c", "#f58e7d", "#c87e96", "#9d7fae", "#3c8eda", "#1d5ae3")) +
  theme_void() +
  theme(plot.background = element_rect(color="grey15", fill="grey15"),
        panel.background = element_rect(color="grey15", fill="grey15"),
        plot.margin=margin(1.5,7,0.5,0, unit="cm"),
        legend.position = "none")

# Annotate
# ggdraw(p1) +
#   draw_label(label="Community Garden", color= "#ffe287", x=labelx, y=0.71, size=labelfontsize, fontfamily=font1, fontface = "bold") +
#   draw_label(label="Library", color= "#ffb47c", x=labelx, y=0.64, size=labelfontsize, fontfamily=font1, fontface = "bold") +
#   draw_label(label="Museum", color= "#f58e7d", x=labelx, y=0.57, size=labelfontsize, fontfamily=font1, fontface = "bold") +
#   draw_label(label="Open Space", color= "#c87e96", x=labelx, y=0.5, size=labelfontsize, fontfamily=font1, fontface = "bold") +
#   draw_label(label="Park", color= "#9d7fae", x=labelx, y=0.43, size=labelfontsize, fontfamily=font1, fontface = "bold") +
#   draw_label(label="Playground", color= "#3c8eda", x=labelx, y=0.36, size=labelfontsize, fontfamily=font1, fontface = "bold") +
#   draw_label(label="Theatre", color= "#1d5ae3", x=labelx, y=0.29, size=labelfontsize, fontfamily=font1, fontface = "bold") +
#   # draw_label(label=paste("Community Spaces in ", borough_name, sep=""), color= "grey90", x=0.5, y=0.95, size=100, fontfamily=font1, fontface = "bold") +
#   # draw_label(label="Twitter: @XXX | Source: NYC Open Data | GitHub: XXX", color= "grey85", x=0.5, y=0.02, size=35, fontface = "bold", fontfamily = font1)

# Save
ggsave(file_path, width = 10, height = 10)
