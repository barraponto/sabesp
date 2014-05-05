casper = require('casper').create(
  logLevel: 'debug',
  verbose: true,
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X)'
)

dates = require './dates.json'
starturl = 'http://www2.sabesp.com.br/mananciais/divulgacaopcj.aspx'

setDate = (date) ->
  return ->
    casper.fill('#form1', {
      'cmbDia': date.day,
      'cmbMes': date.month,
      'cmbAno': date.year,
    }, true)

saveDate = (date) ->
  return -> casper.download(
    casper.evaluate -> return document.getElementById('imgSistema').src
    'source/' + date.year + date.month + date.day + '.jpg'
  )

casper.start starturl, ->
  @each dates, (self, date) ->
    self.then(setDate(date)).then(saveDate(date))

casper.run()
