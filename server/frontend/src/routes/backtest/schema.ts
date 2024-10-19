import { z } from "zod"

export const formSchema = z.object({

    startDate: z.string().date("Invalid date format. use YYYY-MM-DD format"),
    
    endDate: z.string().date("Invalid date format. use YYYY-MM-DD format"),

    investment: z.number().positive("Investment must be a positive number"),
    
    buyRange: z.number().positive("Needs to be positive").min(1),
    
    sellRange: z.number().positive("Needs to be positive").min(1),

})