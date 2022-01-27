'use strict'
const fs = require('fs')

const INPUT_FILE = './data/input.json'
const OUTPUT_FILE = './data/output.json'

function getCommissions(deals) {
  var commissions = 0
  // sum of all deals amount
  const sum = deals.reduce((a, b) => a + b.amount, 0)
  // determine the commission in relation to the number of deals
  commissions = deals.length < 3 ? (commissions = sum * 0.1) : (commissions = sum * 0.2)
  sum > 2000 && (commissions += 500)
  return commissions
}

function main() {
  const data = JSON.parse(fs.readFileSync(INPUT_FILE))
  var output = {}
  output.commissions = data.users.map((user) => ({
    user_id: user.id,
    // get commissions from the user deals
    commission: getCommissions(data.deals.filter((deal) => deal.user === user.id)),
  }))
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(output))
}

main()
