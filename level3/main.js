'use strict'
const fs = require('fs')

const INPUT_FILE = './data/input.json'
const OUTPUT_FILE = './data/output.json'

// return all payed deals at the time of the selected deal close date
function getPayedDeals(deals, deal) {
  const close_date = new Date(deal.close_date)
  return deals.filter(($deal) => new Date($deal.payment_date) <= close_date)
}

function getCommissions(deals, objective) {
  return deals.map((deal) => {
    let commission = 0
    let dealted_amount = 0
    let deal_amount = deal['amount']
    let payed_deals = getPayedDeals(deals, deal).reduce((a, b) => a + b.amount, 0)

    // tier 1 only if the sum of the payed deals amount is lower than the objective and if the deal amount matches perfectly the [0% - 50%] interval
    if (payed_deals <= objective) {
      // if the deal amount is greater than the objective the rest of the amount deal will be commissioned in the next tier
      if (deal_amount > objective * 0.5) {
        commission += objective * 0.5 * (5 / 100)
        deal_amount -= objective * 0.5
        dealted_amount += objective * 0.5
      // otherwise the current tier will be filled in the next deal
      } else {
        commission += deal_amount * (5 / 100)
        deal_amount -= deal_amount
        dealted_amount += deal_amount
      }
    }
    // tier 2 only if the sum of the payed deals amount is lower than the objective and if the deal amount matches perfectly the [50% - 100%] interval
    if (payed_deals <= objective && deal_amount + dealted_amount > objective * 0.5) {
      // same as above
      if (deal_amount > objective * 0.5) {
        commission += objective * 0.5 * 0.1
        deal_amount -= objective * 0.5
        dealted_amount += objective * 0.5
      } else {
        commission += deal_amount * 0.1
        deal_amount -= deal_amount
        dealted_amount += deal_amount
      }
    }
    // tier 3 if the sum of the payed deals amount is greater than the objective OR if the current deal amount already filled the tier 1 and tier 2
    if (payed_deals > objective || deal_amount + dealted_amount > objective) {
      commission += deal_amount * 0.15
    }
    return {
      id: deal.id,
      commission,
      close_date: deal.close_date,
      payment_date: deal.payment_date,
    }
  })
}

function getCommissionsByMonth(deals) {
  // get all deals payment date by month
  var months = deals.map((deal) => deal.payment_date.split('-').slice(0, -1).join('-'))
  // erase duplicate months
  months = [...new Set(months)].sort()
  var commission = {}
  // and get the sum of deals amount for each month
  months.forEach((month) => {
    commission[month] = deals.filter((deal) => deal.payment_date.startsWith(month)).reduce((a, b) => a + b.commission, 0)
  })
  return commission
}

function main() {
  const data = JSON.parse(fs.readFileSync(INPUT_FILE))
  var output = {}
  var deals = []
  var commissions = []
  data.users.forEach((user) => {
    let user_deals = getCommissions(
      data.deals.filter((deal) => deal.user === user.id),
      user.objective
    )
    deals = [...deals, ...user_deals]
    commissions.push({
      user_id: user.id,
      commission: getCommissionsByMonth(user_deals),
    })
  })
  output = {
    commissions,
    // erase the payment_date and the close_date of each deals
    deals: deals.map((deal) => ({ id: deal.id, commission: deal.commission })),
  }
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(output))
}

main()
