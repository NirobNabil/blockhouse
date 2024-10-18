import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

import { ResultsInterface } from "../interfaces/results"


export function ResultCard({ results }: ResultsInterface) {
    return (
        <Card className={cn("w-full  mt-8")}>
            <CardHeader>
                <CardTitle className="py-2">Backtest result</CardTitle>
            </CardHeader>
            <CardContent className="grid">
                <div
                    className="flex mb-4 items-start space-x-2 justify-center pb-4 last:mb-0 last:pb-0"
                >
                    <span className="flex h-2 w-2 translate-y-1 rounded-full bg-sky-500" />
                    <div className="flex w-full justify-between">
                        <p className="text-sm font-medium leading-none">
                            Total return
                        </p>
                        <p className="text-sm leading-none">
                            {results["total_return"]}
                        </p>
                    </div>
                </div>
                <div
                    className="flex mb-4 items-start space-x-2 justify-center pb-4 last:mb-0 last:pb-0"
                >
                    <span className="flex h-2 w-2 translate-y-1 rounded-full bg-sky-500" />
                    <div className="flex w-full justify-between">
                        <p className="text-sm font-medium leading-none">
                            Trade count
                        </p>
                        <p className="text-sm leading-none">
                            {results["trade_count"]}
                        </p>
                    </div>
                </div>
                <div
                    className="flex mb-4 items-start space-x-2 justify-center pb-4 last:mb-0 last:pb-0"
                >
                    <span className="flex h-2 w-2 translate-y-1 rounded-full bg-sky-500" />
                    <div className="flex w-full justify-between">
                        <p className="text-sm font-medium leading-none">
                            Max drawdown
                        </p>
                        <p className="text-sm leading-none">
                            {results["max_drawdown"]}
                        </p>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}