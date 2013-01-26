page = require('webpage').create()

page.onConsoleMessage = (msg) ->
  console.log "got from page: #{msg}"
  return null

page.onLoadFinished = () ->
  #inject jquery
  page.injectJs("lib/jquery.js")

  response = page.evaluate () ->
    #spike window.open
    window.open = (url) ->
      console.log "window.open spike activated with #{url}"
      window.location.href = url
      return null

    el = document.getElementById('PageContent')
    #click the link:
    console.log "clicking the link"
    $(el.children[4].children[0]).click()

    return "SUCCESS"

  if response == "SUCCESS"
    console.log "Completed successfully"
  else
    console.error "Completed unsuccessfully"

  phantom.exit()

  return null


page.open("http://www.gmc-uk.org/doctors/register/LRMP.asp")
