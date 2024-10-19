"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

import { formSchema } from "./schema.ts"
import { Navbar } from "@/components/navbar"
import { API_BASEURL } from "@/constants.ts"



export default function PerformanceReport() {

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      symbol: "AAPL"
    },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    fetch( API_BASEURL + `generate_model_performance/?symbol=${values["symbol"]}`, {
      method: 'GET',
    }).then((r) => r.json()).then(res => {
      // @ts-ignore
      window.open("http://localhost:8000/"+res["pdf"], '_blank').focus()
    })
  }

  // TODO: show server returned errors 
  return (
    <>
      <div className="flex justify-center p-8" >
        <Navbar />
      </div>
      <div className="flex items-center flex-col w-full pt-8" >
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8 min-w-[280px] w-1/2 ">
            <FormField
              control={form.control}
              name="symbol"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Forecast start date: </FormLabel>
                  <FormControl>
                    <Input type="text" {...field} onChange={e => field.onChange(e.target.valueAsNumber)} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button className="w-full" type="submit">Generate performance report</Button>
          </form>
        </Form>
      </div>
    </>
  )
}
