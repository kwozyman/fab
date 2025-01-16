/*
Copyright © 2024 Costin Gament <cos@redhat.com>
*/
package cmd

import (
	"fmt"
	"os"
	"os/exec"

	"github.com/kwozyman/fab/fabpkg"
	"github.com/spf13/cobra"
)

func build(command *cobra.Command, args []string) {
	fileName, err := command.PersistentFlags().GetString("fabfile")
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}
	fabfile, err := fabpkg.ParseFabFileYAML(fileName)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

	podman_extra_args, err := command.PersistentFlags().GetStringSlice("container-tool-extra-args")
	if err != nil {
		fmt.Println("Error: ", err)
		os.Exit(1)
	}

	run_command, _ := command.PersistentFlags().GetString("container-tool")

	previous_container_image := fabfile.From
	for _, module := range fabfile.IncludeModules {
		tag := fabfile.Metadata.Name + "-stage-" + module.Metadata.Name

		var run_args []string

		run_args = append(run_args, podman_extra_args...)

		run_args = append(run_args, "build")
		run_args = append(run_args, "--from")
		run_args = append(run_args, previous_container_image)
		run_args = append(run_args, "--file")
		run_args = append(run_args, module.GetFullContainerfilePath())
		run_args = append(run_args, "--tag")
		run_args = append(run_args, tag)

		for _, kv := range fabfile.BuildArgs {
			for key, value := range kv {
				run_args = append(run_args, "--build-arg")
				run_args = append(run_args, key+"="+value)
			}
		}

		cmd := exec.Command(run_command, run_args...)

		stdoutStderr, err := cmd.CombinedOutput()
		fmt.Printf("%s\n", stdoutStderr)
		if err != nil {
			fmt.Println(err)
			os.Exit(2)
		}

		previous_container_image = tag
	}

	var run_args []string
	run_args = append(run_args, "tag")
	run_args = append(run_args, previous_container_image)
	run_args = append(run_args, fabfile.Metadata.Name)

	cmd := exec.Command(run_command, run_args...)
	stdoutStderr, err := cmd.CombinedOutput()
	fmt.Printf("%s\n", stdoutStderr)
	if err != nil {
		fmt.Println(err)
		os.Exit(-1)
	}
}

// buildCmd represents the build command
var buildCmd = &cobra.Command{
	Use:   "build",
	Short: "Build bootc container",
	Long:  `Build bootc container`,
	Run:   build,
}

func init() {
	rootCmd.AddCommand(buildCmd)
	buildCmd.PersistentFlags().String("fabfile", "Fabfile", "Use this fabfile as input")
	buildCmd.PersistentFlags().String("container-tool", "podman", "What container tool to use")
	buildCmd.PersistentFlags().StringSlice("container-tool-extra-args", nil, "Container tool extra arguments")
}
