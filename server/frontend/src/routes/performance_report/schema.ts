import { z } from "zod"

export const formSchema = z.object({

    symbol: z.enum(["AAPL"]),

})