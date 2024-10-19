import { z } from "zod"

export const formSchema = z.object({

    startDate: z.string().date("Invalid date format. use YYYY-MM-DD format"),
    
    symbol: z.enum(["AAPL"]),

})