'use strict'
const fs = require('fs')

const INPUT_FILE = './data/input.json'
const OUTPUT_FILE = './data/output.json'

function getCommissions(deals, objective) {
  var commissions = 0
  // sum of all deals amount
  var sum = deals.reduce((a, b) => a + b.amount, 0)
  // determine the commission in relation to the objective
  sum > objective * 0.0 && (commissions += objective * 0.5 * 0.05)
  sum > objective * 0.5 && (commissions += objective * 0.5 * 0.1)
  sum > objective * 1.0 && (commissions += (sum -= objective) * 0.15)
  return commissions
}

function main() {
  const data = JSON.parse(fs.readFileSync(INPUT_FILE))
  var output = {}
  output.commissions = data.users.map((user) => ({
    user_id: user.id,
    // get commissions from the user deals and objective
    commission: getCommissions(
      data.deals.filter((deal) => deal.user === user.id),
      user.objective
    ),
  }))
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(output))
}

main()
