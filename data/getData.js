const stations = require('vbb-stations/full.json')
const lines = require('vbb-lines')
var fs = require('fs')

// console.log(stations('900000009101')) // query a single station
// console.log(stations({ // filter by property
// 	weight: 3563,
// 	'location.latitude': 52.542202
// }))

// lines({name: 'S1'}).on('data', console.log)

// lines(true, '15296_700').then(print)


const stationsPerLine = {}

function save(result) {
	// console.log(result)
	// result[0].variants.forEach(function(variant){printVariant(variant)})
	stopIDs = getRelevantVariant(result[0].variants).stops
	stationsPerLine[result[0].name] = stopIDsToNames(stopIDs)

}

function write() {
	console.log('accummulated data: ', stationsPerLine)
	fs.writeFile('lines.json', JSON.stringify(stationsPerLine), function(err) {
		if (err) {
			console.log(err)
		}
	})
}

function getRelevantVariant(variants) {
	var maxTrips = 0
	relevantVariant = null
	variants.forEach(function(variant, index){
		if (variant.trips > maxTrips) {
			maxTrips = variant.trips
			relevantVariant = variant
		}
	})
	return relevantVariant

}

function stopIDsToNames(stopIDs) {
	names = []
	stopIDs.forEach(function(stopID) {
		name = nameForStopID(stopID)
		names.push(name)
	})
	return names
}

function printVariant(variant) {
	// debugger;
	console.log('variant: ', variant)
	variant.stops.forEach(function(station) {
		name = nameForStopID(station)
		
	})
}

function nameForStopID(stopID) {
	data = stations
	for (property in stations) {
		for (stop of stations[property].stops) {
			if (stop.id === stopID) {
				return stations[property].name
			}
		}
	}
	return 'Error: Stop not found!'
	
}


// const stationsPerLine = {}
// subway:
const promises = []
const subwayLines = ['U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9']
subwayLines.forEach(function(subwayLine) {
	const filter = {'name': subwayLine, 'product': 'subway'}
	const promise = lines(true, filter)
	promises.push(promise)
	promise.then(save)
})
Promise.all(promises).then(write)

const suburbanLines = ['S1', 'S2', 'S25', 'S26', 'S3', 'S41', 'S42', 'S45', 'S46', 'S47', 'S5', 'S7', 'S75', 'S8', 'S85', 'S9']
suburbanLines.forEach(function(subwayLine) {
	const filter = {'name': subwayLine, 'product': 'suburban', 'operator': '1'}
	const promise = lines(true, filter)
	promises.push(promise)
	promise.then(save)
})
Promise.all(promises).then(write)

// for subwayLine of subwayLines {
// 	lines(true, {name: subwayLine}).then(console.log)
// 	stationsPerLine[subwayLine] = lines({type: 'bus'}).on('data', console.log)
// }
// // suburban:

