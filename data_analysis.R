library(dplyr, warn.conflicts = F)
library(readr)
library(ggplot2)
theme_set(theme_bw())
library(gmodels)
library(reshape2)

# Reading data from all sources
dados_vagalume = read_csv("Datasets/vagalume_playlists.csv", col_names=TRUE)
dados_8tracks = read_csv("Datasets/8tracks_playlists.csv", col_names=TRUE)
dados_playlists_net = read_csv("Datasets/playlists_net_playlists.csv", col_names=TRUE)
dados_aotm = read_csv("Datasets/aotm_playlists.csv", col_names=TRUE)

# Merging data
full_data = rbind(dados_vagalume, dados_8tracks, dados_playlists_net, dados_aotm)

# Our analysis starts here :)

# Playlists summary
length(unique(full_data$playlist_id))
length(unique(full_data[full_data$source == 'vagalume',]$playlist_id))
length(unique(full_data[full_data$source == 'playlists.net',]$playlist_id))
length(unique(full_data[full_data$source == 'aotm',]$playlist_id))
length(unique(full_data[full_data$source == '8tracks',]$playlist_id))

# Artists summary
length(unique(full_data$artist_name))
length(unique(full_data[full_data$source == 'vagalume',]$artist_name))
length(unique(full_data[full_data$source == 'playlists.net',]$artist_name))
length(unique(full_data[full_data$source == 'aotm',]$artist_name))
length(unique(full_data[full_data$source == '8tracks',]$artist_name))

# Tracks summary
length(unique(full_data$track_name))
length(unique(full_data[full_data$source == 'vagalume',]$track_name))
length(full_data[full_data$source == 'vagalume',]$track_name)
length(unique(full_data[full_data$source == 'playlists.net',]$track_name))
length(full_data[full_data$source == 'playlists.net',]$track_name)
length(unique(full_data[full_data$source == 'aotm',]$track_name))
length(full_data[full_data$source == 'aotm',]$track_name)
length(unique(full_data[full_data$source == '8tracks',]$track_name))
length(full_data[full_data$source == '8tracks',]$track_name)

# Playlists size
mean(data.frame(table(full_data$playlist_id))[,2])
sd(data.frame(table(full_data$playlist_id))[,2])

mean(data.frame(table(dados_8tracks$playlist_id))[,2])
sd(data.frame(table(dados_8tracks$playlist_id))[,2])

mean(data.frame(table(dados_aotm$playlist_id))[,2])
sd(data.frame(table(dados_aotm$playlist_id))[,2])

mean(data.frame(table(dados_playlists_net$playlist_id))[,2])
sd(data.frame(table(dados_playlists_net$playlist_id))[,2])

mean(data.frame(table(dados_vagalume$playlist_id))[,2])
sd(data.frame(table(dados_vagalume$playlist_id))[,2])

# Cool graphs

## Histograms
dados_vagalume[dados_vagalume$genre_rosamerica_value 
               %in% c('pop', 'rhy', 'hip', 'roc', 'dan', 'cla', 'jaz', 'spe'),]%>%
  ggplot(aes(x=reorder(genre_rosamerica_value,genre_rosamerica_value,
                       function(x)-length(x)))) + xlab('Genre') +
  geom_bar() + theme(axis.text=element_text(size=14),
                    axis.title=element_text(size=16))

ggsave("/home/felipe/Desktop/vagalume_genre_histogram.pdf")

dados_8tracks[dados_8tracks$genre_rosamerica_value 
               %in% c('pop', 'rhy', 'hip', 'roc', 'dan', 'cla', 'jaz', 'spe'),]%>%
  ggplot(aes(x=reorder(genre_rosamerica_value,genre_rosamerica_value,
                       function(x)-length(x)))) + xlab('Genre') +
  geom_bar() + theme(axis.text=element_text(size=14),
                    axis.title=element_text(size=16))

ggsave("/home/felipe/Desktop/8tracks_genre_histogram.pdf")

dados_aotm[dados_aotm$genre_rosamerica_value 
              %in% c('pop', 'rhy', 'hip', 'roc', 'dan', 'cla', 'jaz', 'spe'),]%>%
  ggplot(aes(x=reorder(genre_rosamerica_value,genre_rosamerica_value,
                       function(x)-length(x)))) + xlab('Genre') +
  geom_bar() + theme(axis.text=element_text(size=14),
                    axis.title=element_text(size=16))

ggsave("/home/felipe/Desktop/aotm_genre_histogram.pdf")

dados_playlists_net[dados_playlists_net$genre_rosamerica_value 
           %in% c('pop', 'rhy', 'hip', 'roc', 'dan', 'cla', 'jaz', 'spe'),]%>%
  ggplot(aes(x=reorder(genre_rosamerica_value,genre_rosamerica_value,
                       function(x)-length(x)))) + xlab('Genre') +
  geom_bar() + theme(axis.text=element_text(size=14),
                    axis.title=element_text(size=16))

ggsave("/home/felipe/Desktop/playlists_net_genre_histogram.pdf")

full_data[full_data$genre_rosamerica_value 
                    %in% c('pop', 'rhy', 'hip', 'roc', 'dan', 'cla', 'jaz', 'spe'),]%>%
  ggplot(aes(x=reorder(genre_rosamerica_value,genre_rosamerica_value,
                       function(x)-length(x)))) + xlab('Genre') +
  geom_bar() + theme(axis.text=element_text(size=14),
                    axis.title=element_text(size=16))

ggsave("/home/felipe/Desktop/full_data_genre_histogram.pdf")

## Boxplots

aotm_df = data.frame(table(dados_aotm$playlist_id))
aotm_df['source'] = 'aotm'
eight_tracks_df = data.frame(table(dados_8tracks$playlist_id))
eight_tracks_df['source'] = '8tracks'
vagalume_df = data.frame(table(dados_vagalume$playlist_id))
vagalume_df['source'] = 'vagalume'
playlist_net_df = data.frame(table(dados_playlists_net$playlist_id))
playlist_net_df['source'] = 'playlists.net'

expanded_df = rbind(aotm_df, eight_tracks_df, vagalume_df, playlist_net_df)

sample(expanded_df, 20, replace=TRUE) %>%
  ggplot(aes(x = source, y = Freq, fill = source)) +
  geom_boxplot(outlier.shape=NA) + theme(legend.position="top") +
  coord_cartesian(ylim = c(0, 210)) + scale_fill_grey() +
  xlab('Playlist source') +
  ylab('Playlist size') + theme(axis.text=element_text(size=14),
                            axis.title=element_text(size=12))

ggsave("/home/felipe/Desktop/playlist_size_boxplot.pdf")


dados_playlists_net[dados_playlists_net$mood_happy_value 
          %in% c('pop', 'rhy', 'hip', 'roc', 'dan', 'cla', 'jaz', 'spe'),]%>%
  ggplot(aes(x=reorder(genre_rosamerica_value,genre_rosamerica_value,
                       function(x)-length(x)))) + xlab('Genre') +
  geom_bar() + theme(axis.text=element_text(size=14),
                     axis.title=element_text(size=16))



happiness_aotm_df = rbind(subset(dados_aotm, dados_aotm$mood_happy_value=='happy'), subset(dados_aotm, dados_aotm$mood_sad_value=='sad'))
happiness_8tracks_df = rbind(subset(dados_8tracks, dados_8tracks$mood_happy_value=='happy'), subset(dados_8tracks, dados_8tracks$mood_sad_value=='sad'))
happiness_vagalume_df = rbind(subset(dados_vagalume, dados_vagalume$mood_happy_value=='happy'), subset(dados_vagalume, dados_vagalume$mood_sad_value=='sad'))
happiness_playlists_net = rbind(subset(dados_playlists_net, dados_playlists_net$mood_happy_value=='happy'), subset(dados_playlists_net, dados_playlists_net$mood_sad_value=='sad'))

happiness_aotm_df[happiness_aotm_df$mood_happy_value,]%>%
  ggplot(aes(x=reorder(mood_happy_value,mood_happy_value,
                       function(x)-length(x)))) + xlab('Genre') +
  geom_bar() + theme(axis.text=element_text(size=14),
                     axis.title=element_text(size=16))

happiness = subset(full_data, mood_happy_value == 'happy' | mood_sad_value == 'sad')

ggplot(aes(x = source, y = Freq, fill = source)) + 
  geom_bar(aes(fill = source)) + 
  scale_fill_manual(values=c("Blue", "Red")) + 
  facet_wrap( ~ source)