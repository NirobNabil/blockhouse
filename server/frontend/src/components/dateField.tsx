"use client"

import { format } from "date-fns"
import { Calendar as CalendarIcon } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { Input } from "@/components/ui/input"


export function DatePickerField( {field}:any ) {

  return (
    <Popover>
      <div 
        className={cn(
          "justify-start text-left font-normal flex",
        )}
      >
        <Input
          className={cn("rounded-r-none")}
          {...field}
        />
        <PopoverTrigger asChild>
          <Button className={cn("rounded-l-none")} >
            <CalendarIcon className="h-4 w-4" />
          </Button>
        </PopoverTrigger>
      </div>
      
      <PopoverContent className="w-auto p-0">
        <Calendar
          mode="single"
          selected={field.value}
          onSelect={ (date: Date | undefined) => field.onChange( format(date || field.value, "yyyy-MM-dd") )}
        />
      </PopoverContent>
    </Popover>
  )
}
