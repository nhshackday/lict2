page = require('webpage').create()

page.onLoadFinished = (status) ->
  console.log ("loaded: " + status)
  console.log page.evaluate( () ->
    return window.document.title
  )
  page.switchToChildFrame("frame1")
  console.log page.evaluate( () ->
    return window.document.title
  )
  return null


page.open("http://localhost:4000/test/webpage-spec-frames/index.html")
