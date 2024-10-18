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

import { formSchema } from "./schema"
import { DatePickerField } from "./components/dateField"
import { ResultCard } from "./components/resultCard"

export default function ProfileForm() {
  
  const [results, setResults] = useState({'total_return': 0, 'trade_count': 0, 'max_drawdown': 0})

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      startDate: '2012-01-01',
      endDate: '2024-10-01',
      investment: 5000,
      buyRange: 50,
      sellRange: 200,
    },
  })
 
  function onSubmit(values: z.infer<typeof formSchema>) {
    fetch('http://localhost:8000/api/backtest/', {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({
        ...values
      })
    }).then( (r) => r.json() ).then( res => {
      let total_return:number = parseFloat(res["total_return"]);
      let trade_count:number = parseFloat(res["trade_count"]);
      let max_drawdown:number = parseFloat(res["max_drawdown"]);
      setResults( {total_return, trade_count, max_drawdown} )
    } )
  }

  // TODO: show server returned errors 
  return (
    <div className="flex items-center flex-col w-full pt-8" >
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8 min-w-[280px] w-1/2 ">
        <FormField
          control={form.control}
          name="investment"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Initial investment amount: </FormLabel>
              <FormControl>
                <Input type="number" {...field} onChange={ e => field.onChange( e.target.valueAsNumber) } />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="buyRange"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Moving average range for buy: </FormLabel>
              <FormControl>
                <Input type="number" {...field} onChange={ e => field.onChange( e.target.valueAsNumber) } />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="sellRange"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Moving average range for sell: </FormLabel>
              <FormControl>
                <Input type="number" {...field} onChange={ e => field.onChange( e.target.valueAsNumber) } />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="startDate"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Backtest start date: </FormLabel>
              <FormControl>
                <DatePickerField field={field} />
                {/* <Input placeholder="shadcn" {...field} /> */}
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="endDate"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Backtest end date: </FormLabel>
              <FormControl>
                <DatePickerField field={field} />
                {/* <Input placeholder="shadcn" {...field} /> */}
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button className="w-full" type="submit">Submit</Button>
      </form>
    </Form>
    <div className="min-w-[280px] w-1/2 " >
      <ResultCard results={results} />
    </div>
    </div>
  )
}
