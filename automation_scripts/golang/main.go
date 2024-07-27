// GOAL: Measure Throughput & Latency
// SCENARIO basic: 1 Producer  & 1 Consumer with non- durable messages
// SCENARIO optimized : 1 Producer & 1 Consumer with durable messages and manual acks

package main

import (
	"flag"
	"fmt"
	scenario_1 "project/basic_scenarios/scenario_1"
	global "project/global"
)

func main() {

	scenarioPtr := flag.String("scenario", "scenario_0", "select scenario name")
	consOrPtr := flag.String("role", "consumer", "Select if producer or consumer should be launched")
	messageAmountPtr := flag.Int("message_amount", 1, "How many messages should be sent?")

	flag.Parse()

	// mapping scenarios to roles and functions
	type ScenarioFunc func(interface{})

	var scenarios = map[string]map[string]ScenarioFunc{
		"scenario_1": {
			"producer": func(params interface{}) { scenario_1.RunProducerBasic(params.(global.Scenario1Params)) },
			"consumer": func(params interface{}) { scenario_1.RunConsumerBasic() },
		},
		// Zuz plz add more scenarios here later
	}

	scenario, scenarioExsists := scenarios[*scenarioPtr]

	if !scenarioExsists {
		fmt.Println("Invalid scenario selected!")
		return
	}

	roleFunc, roleExists := scenario[*consOrPtr]
	if !roleExists {
		fmt.Println("Invalid role selected")
		return
	}

	// Prepare parameters based on scenario
	var params interface{}

	switch *scenarioPtr {
	case "scenario_1":

		params = global.Scenario1Params{
			MessageAmount: *messageAmountPtr,
		}

		fmt.Printf("selected: %v", *scenarioPtr)

	case "scenario_2":
		fmt.Printf("selected: %v", *scenarioPtr)

	case "scenario_3":
		fmt.Printf("selected: %v", *scenarioPtr)

	default:
		fmt.Printf("Didn't chose any scenario")
	}

	roleFunc(params)

}
