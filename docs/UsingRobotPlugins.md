# Using ROBOT Plugins

Since version 1.9.5, the ROBOT tool allows to use [plugins](http://robot.obolibrary.org/plugins) that provide supplementary commands that are not part of the default command set.

## Declaring the plugins to be used

Before you can use plugins in a custom workflow, the ODK must be aware of those plugins. There are several ways to do that.

### Listing the plugins in the ODK configuration

Add a new `robot_plugins` section to your ODK configuration file (`src/ontology/ONT-odk.yaml`). That section should contain a single `plugins` key, which itself should contain the list of the plugins you want to use. Each entry in the list must contain at least a `name` key, which is the name under which the plugin will be available, and optionally a `mirror_from` key, pointing to an online location from which the plugin can be downloaded.

For example, to use the [KGCL](https://github.com/gouttegd/kgcl-java/) plugin:

```yaml
robot_plugins:
  plugins:
    - name: kgcl
      mirror_from: https://github.com/gouttegd/kgcl-java/releases/download/kgcl-0.2.0/kgcl-robot-plugin-0.2.0.jar
```

If you do not specify a download location with the `mirror_from` key, a dummy rule `${ROBOT_PLUGINS_DIRECTORY}/kgcl.jar` will be generated in the standard Makefile. You will need to override that rule in your ontology-specific Makefile:

```Make
${ROBOT_PLUGINS_DIRECTORY}/kgcl.jar:
    curl -L -o $@ https://github.com/gouttegd/kgcl-java/releases/download/kgcl-0.2.0/kgcl-robot-plugin-0.2.0.jar
```


### Using custom rules

If for whatever reason you do not want to modify your ODK configuration, you can still set up a plugin by adding a rule such as the one above in the custom Makefile, and listing the plugin in the `custom_robot_plugins` variable. For example, again with the KGCL lplugin:

```Make
${ROBOT_PLUGINS_DIRECTORY}/kgcl.jar:
    curl -L -o $@ https://github.com/gouttegd/kgcl-java/releases/download/kgcl-0.2.0/kgcl-robot-plugin-0.2.0.jar

custom_robot_plugins: $(ROBOT_PLUGINS_DIRECTORY)/kgcl.jar
```


### Putting the plugin file in the top-level `plugins` directory

Any Jar file found in the repository’s top-level `plugins` directory (if such a directory exists) will automatically be found by the ODK, without requiring any change to the ODK configuration or the custom Makefile.


### ODK-provided plugins

Some plugins are already bundled with the ODK and don’t need to be declared or downloaded from somewhere else. For now, there is only one such plugin: the [SSSOM plugin](https://github.com/gouttegd/sssom-java/). More default plugins may be added in future ODK versions.


## Using a plugin a custom workflow

Any Make rule that involves the use of a ROBOT plugin MUST depend on the `all_robot_plugins` target. This will ensure that all plugins have been properly set up in the runtime ROBOT plugins directory.
