var OfficeApp = angular.module('OfficeApp', ['ngRoute', 'ngResource', 'contenteditable']);

OfficeApp.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{!');
    $interpolateProvider.endSymbol('!}');
}]);

OfficeApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('meta[name=csrf-token]').attr('content');
});

OfficeApp.config(function($resourceProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;
});

OfficeApp.factory("Users", function($resource) {
    return $resource(
        "/users/:id/",
        { id: "@id" },
        {
            'create': { method: 'POST' },
            'list': { method: 'GET', isArray: true },
            'get': { method: 'GET', isArray: false },
            'update': { method: 'PUT' },
            'delete': { method: 'DELETE' }
        }
    );
});

OfficeApp.factory("Rooms", function($resource) {
    return $resource(
        "/rooms/:id/",
        { id: "@id" },
        {
            'create': { method: 'POST' },
            'list': { method: 'GET', isArray: true },
            'get': { method: 'GET', isArray: false },
            'update': { method: 'PUT' },
            'delete': { method: 'DELETE' }
        }
    );
});

OfficeApp.factory("Core", function($http) {
    return {
        'clear_form_errors': function(form_class) {
            $('form.'+form_class).find('div.error').each(function(index, element) {
                $(element).removeClass('error');
            });
            $('form.'+form_class).find('div.input_errors').each(function(index, element) {
                $(element).remove();
            });
        },
        'set_fields_label': function($scope, url) {
            var req = {
                method: 'OPTIONS',
                url: url,
                headers: {
                    'Content-Type': 'application/json'
                },
            }

            $http(req)
            .success(
                function(data) {
                var keys = Object.keys(data.actions.POST);
                keys.forEach(function(element, index, array) {
                    $scope[element+'_label'] = data.actions.POST[element].label;
                });
            }
            ).error(
            function(){}
            );
        },
        'assign': function(obj, prop, value) {
            if (typeof prop === "string")
                prop = prop.split(".");

            if (prop.length > 1) {
                var e = prop.shift();
                assign(obj[e] =
                       Object.prototype.toString.call(obj[e]) === "[object Object]"
                           ? obj[e]
                           : {},
                           prop,
                           value);
            } else
                obj[prop[0]] = value;
        },
    }
});

OfficeApp.controller('UsersController', ['$scope', '$filter', '$routeParams', '$http', 'Users', 'Core', function($scope, $filter, $routeParams, $http, Users, Core) {
    $scope.items = Users.list();
    $scope.controller_name = 'Пользователи';
    $scope.user = new Users();

    Core.set_fields_label($scope, '/users/');

    // save new record
    $scope.submit = function() {
        Core.clear_form_errors('users');
        $scope.user.date_joined = $filter('date')($scope.user.date_joined, 'yyyy-MM-dd');
        $scope.user.$create(
            function(data, response) {
                $scope.items.push(data);
                $scope.user = new Users();
                Core.clear_form_errors('users');
            },
            function(response) {
                var keys = Object.keys(response.data);

                keys.forEach(function(element, index, array) {
                    var input = $('form.users').find('input[name="'+element+'"]');
                    input.parent('div').addClass('error');
                    input.after('<div class="ui red pointing prompt label transition visible error input_errors">' + response.data[element] + '</div>');
                });
            }
        );
    };

    // delete record
    $scope.remove = function(item) {
        Users.delete({'id': item.id}, function() {
            var index = $scope.items.indexOf(item)
            $scope.items.splice(index, 1);
        });
    };

    // show input with datepicker
    $scope.edit_datepicker = function(id) {
        Core.assign($scope, 'show_datepicker_'+id, true);
    }

    // update data and hide input with datepicker
    $scope.save_datepicker = function(item) {
        item.date_joined = $filter('date')(item.date_joined, 'yyyy-MM-dd');
        item.$update(function() {
            Core.assign($scope, 'show_datepicker_'+item.id, false);
        });
    }
}]);

OfficeApp.controller('RoomsController', ['$scope', '$routeParams', 'Rooms', 'Core', function($scope, $routeParams, Rooms, Core) {
    $scope.items = Rooms.list();
    $scope.controller_name = 'Комнаты';
    $scope.room = new Rooms();

    Core.set_fields_label($scope, '/rooms/');

    // save new record
    $scope.submit = function() {
        Core.clear_form_errors('rooms');
        $scope.room.$create(
            function(data, response) {
                $scope.items.push(data);
                $scope.room = new Rooms();
                Core.clear_form_errors('rooms');
            },
            function(response) {
                var keys = Object.keys(response.data);

                keys.forEach(function(element, index, array) {
                    var input = $('form.rooms').find('input[name="'+element+'"]');
                    input.parent('div').addClass('error');
                    input.after('<div class="ui red pointing prompt label transition visible error input_errors">' + response.data[element] + '</div>');
                });
            });
    };

    // delete record
    $scope.remove = function(item) {
        Rooms.delete({'id': item.id}, function() {
            var index = $scope.items.indexOf(item)
            $scope.items.splice(index, 1);
        });
    };
}]);

OfficeApp.config(['$routeProvider', function ($routeProvider, $locationProvider) {
    $routeProvider.when('/office/users/', {
        templateUrl: 'users.html',
        controller: 'UsersController'
    });

    $routeProvider.when('/office/rooms/', {
        templateUrl: 'rooms.html',
        controller: 'RoomsController'
    });

}]);
