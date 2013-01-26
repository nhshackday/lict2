require 'sinatra'
require 'json'

require 'pry'

#  from lict2/lrmp_scraper/test   run with `ruby sinatraApp.rb -p 4000`


#not in use, if we run into trouble navigating frames then we'll come back here to learn

get '/frame2-3.html' do
  sleep 10
  send_file File.join(File.dirname(__FILE__), "/webpage-spec-frames/frame2-3.html")
end

get '/:file' do
  send_file File.join(File.dirname(__FILE__), "/webpage-spec-frames/#{params[:file]}")
end