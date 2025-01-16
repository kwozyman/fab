/*
Copyright © 2024 Costin Gament <cgament@redhat.com>
*/
package cmd

import (
	"os"

	"github.com/spf13/cobra"
)

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "fab",
	Short: "Fast Assembler for Bootc",
	Long:  `fab is a somewhat opinionated build pipeline for bootc, allowing the modularization of Containerfiles/bootc image building.`,
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	// Here you will define your flags and configuration settings.
}
