"use client"

import { Link } from "react-router-dom";

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"


export function Navbar() {
  return (
    <NavigationMenu>
      <NavigationMenuList>
        <NavigationMenuItem>
          <Link to="/update_database">
            <NavigationMenuLink className={navigationMenuTriggerStyle()}>
              Update database
            </NavigationMenuLink>
          </Link>
        </NavigationMenuItem>
        
        <NavigationMenuItem>
          <Link to="/backtest_results">
            <NavigationMenuLink className={navigationMenuTriggerStyle()}>
              Backtest results
            </NavigationMenuLink>
          </Link>
        </NavigationMenuItem>
        <NavigationMenuItem>
          <Link to="/backtest">
            <NavigationMenuLink className={navigationMenuTriggerStyle()}>
              Backtest
            </NavigationMenuLink>
          </Link>
        </NavigationMenuItem>
        <NavigationMenuItem>
          <Link to="/forecast">
            <NavigationMenuLink className={navigationMenuTriggerStyle()}>
              Forecast
            </NavigationMenuLink>
          </Link>
        </NavigationMenuItem>
      <NavigationMenuItem>
          <Link to="/performance_report">
            <NavigationMenuLink className={navigationMenuTriggerStyle()}>
              Performance report
            </NavigationMenuLink>
          </Link>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>
  )
}

