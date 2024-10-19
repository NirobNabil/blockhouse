"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { useState } from "react"

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



export default function UpdateDatabase() {

  const [ result, setResult ] = useState("")

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      symbol: "AAPL"
    },
  })

  // TODO: Error handling
  function onSubmit(values: z.infer<typeof formSchema>) {
    setResult("Updating database. please wait...")
    fetch( API_BASEURL + `generate_model_performance/?symbol=${values["symbol"]}`, {
      method: 'GET',
    }).then((r) => {
      if( !r.ok ) {
        return r.text().then( text => { throw new Error(text) } )
      } else {
        return r.text()
      }
    }).then(res_text => {
      setResult(res_text)
    }).catch(err => {
      setResult(err)
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
            <Button className="w-full" type="submit">Update database</Button>
          </form>
        </Form>
        <div>{result}</div>
      </div>
    </>
  )
}
